# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
import bpy

bl_info = {
    "name": "Rigify Picker",
    "author": "dskjal",
    "version": (2, 0),
    "blender": (2, 78, 0),
    "location": "Properties Shelf",
    "description": "Rigify Picker",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Rigging"
}

#-------------------------------------- Helper functions ----------------------------------------------------
def boneNameToClassName(name):
    return name.replace('.','d').replace('_','a').lower()

def boneNameToOperatorName(name):
    return "dskjal."+boneNameToClassName(name)

def createButton(name):
    code = 'class %sButton(bpy.types.Operator):\n' % (boneNameToClassName(name))
    code +='  bl_idname = "%s"\n' % (boneNameToOperatorName(name))
    code +='  bl_label = "%s"\n' % (name)
    code +='  def execute(self, context):\n'
    code +='    bpy.ops.pose.select_all(action="DESELECT")\n'
    code +='    o = context.active_object\n'
    code +='    o.data.bones["%s"].select = True\n' % (name)

    #auto ik/fk switch
    code +='    if not context.active_object.is_auto_ikfk_select:\n'
    code +='      return {"FINISHED"}\n'
    lr = name[-2:]
    if name.find('ik') != -1:
        code += '    if isPitchipoy():\n'
        if name.find('elbow') != -1 or name.find('hand') != -1 or name.find('arm') != -1:
            code +='      o.pose.bones["MCH-upper_arm_parent'+lr+'"]["IK/FK"] = 0\n'
            code +='    else:\n'
            code +='      o.pose.bones["hand.ik'+lr+'"]["ikfk_switch"] = 1\n'
        else:
            code +='      o.pose.bones["MCH-thigh_parent'+lr+'"]["IK/FK"] = 0\n'
            code +='    else:\n'
            code +='      o.pose.bones["foot.ik'+lr+'"]["ikfk_switch"] = 1\n'

    elif name.find('fk') != -1:
        code += '    if isPitchipoy():\n'
        if name.find('arm') != -1 or name.find('hand') != -1:
            code +='      o.pose.bones["MCH-upper_arm_parent'+lr+'"]["IK/FK"] = 1\n'
            code +='    else:\n'
            code +='      o.pose.bones["hand.ik'+lr+'"]["ikfk_switch"] = 0\n'
        else:
            code +='      o.pose.bones["MCH-thigh_parent'+lr+'"]["IK/FK"] = 1\n'
            code +='    else:\n'
            code +='      o.pose.bones["foot.ik'+lr+'"]["ikfk_switch"] = 0\n'

    code +='    return{"FINISHED"}\n\n'
    return code


def createSelectPartsButton(name):
    return '''
class %sButton(bpy.types.Operator):
  bl_idname = "%s"
  bl_label = "%s"
  def execute(self, context):
    bpy.ops.pose.select_all(action="DESELECT")
    for boneName in %s:
      context.active_object.data.bones[boneName].select = True
    return{"FINISHED"}
''' % (boneNameToClassName(name), boneNameToOperatorName(name), name, name)

def createKeyframeAllButton(name,properties):
    return '''
class %sButton(bpy.types.Operator):
  bl_idname = "%s"
  bl_label = "%s"
  def execute(self, context):
    for boneName in %s:
      b = bpy.context.active_object.pose.bones[boneName]
      b.keyframe_insert(data_path="location",group=boneName)
      if b.rotation_mode == "QUATERNION":
        b.keyframe_insert(data_path="rotation_quaternion",group=boneName)
      elif b.rotation_mode == "AXIS_ANGLE":
        b.keyframe_insert(data_path="rotation_axis_angle",group=boneName)
      else:
        b.keyframe_insert(data_path="rotation_euler",group=boneName)
      b.keyframe_insert(data_path="scale",group=boneName)
    for boneName, props in %s:
      for p in props:
        path = \'pose.bones["\' + boneName + \'"]["\' + p + \'"]\'
        context.active_object.pose.bones[boneName].id_data.keyframe_insert(data_path=path)
    return{"FINISHED"}
''' % (boneNameToClassName(name), boneNameToOperatorName(name), name, name, properties)


def isPitchipoy():
    try:
        return bpy.context.active_object.data.bones['tweak_spine.005'] != None
    except:
        return False

#---------------------------------------- Button Generator (Update if Rigify updated) ----------------------------------------------------
metarigBoneNames = ["head",
                    "neck",
                    "shoulder.R", "shoulder.L", #3
                    "upper_arm_hose_end.R", "upper_arm_hose.R", "elbow_hose.R", "forearm_hose.R", "forearm_hose_end.R",#8
                    "elbow_target.ik.R", "upper_arm.fk.R", "forearm.fk.R", "chest", "spine", "torso", "hips", "upper_arm.fk.L", "forearm.fk.L", "elbow_target.ik.L",#18
                    "upper_arm_hose_end.L", "upper_arm_hose.L", "elbow_hose.L", "forearm_hose.L", "forearm_hose_end.L",#23
                    "palm.R", "hand.ik.R", "hand.fk.R",#26
                    "f_pinky.R", "f_ring.R", "f_middle.R", "f_index.R", "thumb.R",#31
                    "thigh.fk.R", "thigh.fk.L", "palm.L", "hand.fk.L", "hand.ik.L",#36
                    "thumb.L", "f_index.L", "f_middle.L", "f_ring.L", "f_pinky.L",#41
                    "thigh_hose_end.R", "thigh_hose.R", "knee_hose.R", "shin_hose.R", "shin_hose_end.R",#46
                    "knee_target.ik.R", "shin.fk.R", "shin.fk.L", "knee_target.ik.L",#50
                    "thigh_hose_end.L", "thigh_hose.L", "knee_hose.L", "shin_hose.L", "shin_hose_end.L",#55
                    "foot.ik.R", "foot.fk.R", "foot.fk.L", "foot.ik.L",#59
                    "toe.R", "foot_roll.ik.R", "foot_roll.ik.L", "toe.L",#63
                    "root"
]

pitchipoyBoneNames = ["head", "tweak_spine.005", "neck", "tweak_spine.004", "chest",#4
                      "shoulder.R", "shoulder.L",#6
                      "upper_arm_tweak.R", "upper_arm_tweak.R.001", "forearm_tweak.R", "forearm_tweak.R.001", "hand_tweak.R",#11
                      "upper_arm_ik.R", "upper_arm_fk.R", "forearm_fk.R", "breast.R",#15
                      "tweak_spine.003", "tweak_spine.002", "tweak_spine.001", "tweak_spine",#19
                      "breast.L", "upper_arm_fk.L", "forearm_fk.L", "upper_arm_ik.L",#23
                      "upper_arm_tweak.L", "upper_arm_tweak.L.001", "forearm_tweak.L", "forearm_tweak.L.001", "hand_tweak.L",#28
                      "palm.R", "hand_ik.R", "hand_fk.R",#31
                      "f_pinky.01.R", "f_pinky.02.R", "f_pinky.03.R",#34
                      "f_ring.01.R", "f_ring.02.R", "f_ring.03.R",#37
                      "f_middle.01.R", "f_middle.02.R", "f_middle.03.R",#40
                      "f_index.01.R", "f_index.02.R", "f_index.03.R",#43
                      "thumb.01.R", "thumb.02.R", "thumb.03.R",#46
                      "torso", "hips",#48
                      "palm.L", "hand_fk.L", "hand_ik.L",#51
                      "thumb.01.L", "thumb.02.L", "thumb.03.L",#54
                      "f_index.01.L", "f_index.02.L", "f_index.03.L",#57
                      "f_middle.01.L", "f_middle.02.L", "f_middle.03.L",#60
                      "f_ring.01.L", "f_ring.02.L", "f_ring.03.L",#63
                      "f_pinky.01.L", "f_pinky.02.L", "f_pinky.03.L",#66
                      "thigh_tweak.R", "thigh_tweak.R.001", "shin_tweak.R", "shin_tweak.R.001", "foot_tweak.R",#71
                      "thigh_ik.R",#72
                      "thigh_fk.R", "shin_fk.R", "thigh_fk.L", "shin_fk.L",#76
                      "thigh_ik.L",#77
                      "thigh_tweak.L", "thigh_tweak.L.001", "shin_tweak.L", "shin_tweak.L.001", "foot_tweak.L",#82
                      "foot_ik.R", "foot_fk.R", "foot_fk.L", "foot_ik.L",#86
                      "toe.R", "foot_heel_ik.R", "foot_heel_ik.L", "toe.L",#90
                      "root"
]

#select all indices
def generateFingerList(suffix,isPitchipoy=False):
    out = []
    nameList = ["thumb", "f_index", "f_middle", "f_ring", "f_pinky"]
    numList = [".01", ".02", ".03"]
    if isPitchipoy:
        for name in nameList:
            for i in numList:
                out.append('tweak_'+name+i+suffix)
            out.append('tweak_'+name+numList[-1]+suffix+'.001')
    else:
        for name in nameList:
            for i in numList:
                out.append(name+i+suffix)

    return out

metarigArmRNames = generateFingerList(".R") + metarigBoneNames[4:12] + metarigBoneNames[24:32]
metarigArmLNames = generateFingerList(".L") + metarigBoneNames[16:24] + metarigBoneNames[34:42]
metarigLegRNames = [metarigBoneNames[32]] + metarigBoneNames[42:49] + metarigBoneNames[56:58] + metarigBoneNames[60:62]
metarigLegLNames = [metarigBoneNames[33]] + metarigBoneNames[49:56] + metarigBoneNames[62:64] + metarigBoneNames[58:60]

pitchipoyArmRNames = generateFingerList(".R", isPitchipoy=True) + pitchipoyBoneNames[7:15] + pitchipoyBoneNames[29:47]
pitchipoyArmLNames = generateFingerList(".L", isPitchipoy=True) + pitchipoyBoneNames[21:29] + pitchipoyBoneNames[49:67]
pitchipoyLegRNames = pitchipoyBoneNames[67:75] + pitchipoyBoneNames[83:85] + pitchipoyBoneNames[87:89]
pitchipoyLegLNames = pitchipoyBoneNames[75:83] + pitchipoyBoneNames[85:87] + pitchipoyBoneNames[89:91]


#for keyframe
metarigAllBoneNames   = generateFingerList(".R") + generateFingerList(".L") + metarigBoneNames
pitchipoyAllBoneNames = generateFingerList(".R", isPitchipoy=True) + generateFingerList(".L", isPitchipoy=True) + pitchipoyBoneNames
metarigAllPropertyNames = [("head",["isolate", "neck_follow"]), ("torso", ["pivot_slide"]), ("spine",["auto_rotate"]),
                           ("upper_arm.fk.R", ["isolate","stretch_length"]), ("hand.ik.R",["ikfk_switch", "stretch_length", "auto_stretch"]), ("elbow_target.ik.R",["follow"]), ("elbow_hose.R",["smooth_bend"]),
                           ("upper_arm.fk.L", ["isolate","stretch_length"]), ("hand.ik.L",["ikfk_switch", "stretch_length", "auto_stretch"]), ("elbow_target.ik.L",["follow"]), ("elbow_hose.L",["smooth_bend"]),
                           ("thigh.fk.R",["isolate", "stretch_length"]), ("foot.ik.R",["ikfk_switch", "stretch_length", "auto_stretch"]), ("knee_target.ik.R",["follow"]), ("knee_hose.R",["smooth_bend"]),
                           ("thigh.fk.L",["isolate", "stretch_length"]), ("foot.ik.L",["ikfk_switch", "stretch_length", "auto_stretch"]), ("knee_target.ik.L",["follow"]), ("knee_hose.L",["smooth_bend"])
                           ]
pitchipoyAllPropertyNames = [("torso",["head_follow", "neck_follow"]),
                             ("MCH-upper_arm_parent.R",["IK/FK", "FK_limb_follow", "IK_Strertch"]), ("upper_arm_tweak.R.001", ["rubber_tweak"]), ("forearm_tweak.R", ["rubber_tweak"]), ("forearm_tweak.R.001", ["rubber_tweak"]), ("forearm_tweak.R",["rubber_tweak"]),
                             ("MCH-upper_arm_parent.L",["IK/FK", "FK_limb_follow", "IK_Strertch"]), ("upper_arm_tweak.L.001", ["rubber_tweak"]), ("forearm_tweak.L", ["rubber_tweak"]), ("forearm_tweak.L.001", ["rubber_tweak"]), ("forearm_tweak.L",["rubber_tweak"]),
                             ("MCH-thigh_parent.R",["IK/FK", "FK_limb_follow", "IK_Strertch"]), ("thigh_tweak.R.001", ["rubber_tweak"]), ("shin_tweak.R", ["rubber_tweak"]), ("shin_tweak.R.001",["rubber_tweak"]),
                             ("MCH-thigh_parent.L",["IK/FK", "FK_limb_follow", "IK_Strertch"]), ("thigh_tweak.L.001", ["rubber_tweak"]), ("shin_tweak.L", ["rubber_tweak"]), ("shin_tweak.L.001",["rubber_tweak"]),
                             ("jaw_master", ["mouth_lock"]), ("eyes", ["eyes_follow"])]

#generate buttons
generatedButtonCode = ""
for i in metarigBoneNames:
    generatedButtonCode += createButton(i)
for i in pitchipoyBoneNames:
    generatedButtonCode += createButton(i)
exec(generatedButtonCode)

#generate all select buttons
exec(createSelectPartsButton("metarigArmRNames"))
exec(createSelectPartsButton("metarigArmLNames"))
exec(createSelectPartsButton("metarigLegRNames"))
exec(createSelectPartsButton("metarigLegLNames"))
exec(createSelectPartsButton("pitchipoyArmRNames"))
exec(createSelectPartsButton("pitchipoyArmLNames"))
exec(createSelectPartsButton("pitchipoyLegRNames"))
exec(createSelectPartsButton("pitchipoyLegLNames"))

#generate keyframe all buttons
exec(createKeyframeAllButton("metarigAllBoneNames", "metarigAllPropertyNames"))
exec(createKeyframeAllButton("pitchipoyAllBoneNames", "pitchipoyAllPropertyNames"))


#cache operator names for performance
metarigOperatorNames = []
for name in metarigBoneNames:
    metarigOperatorNames.append(boneNameToOperatorName(name))

pitchipoyOperatorNames = []
for name in pitchipoyBoneNames:
    pitchipoyOperatorNames.append(boneNameToOperatorName(name))

#---------------------------------------- UI --------------------------------------------------
class UI(bpy.types.Panel):
  bl_label = "Rigify Picker"
  bl_space_type = "VIEW_3D"
  bl_region_type = "UI"

  bpy.types.Object.is_auto_ikfk_select = bpy.props.BoolProperty(name="",default=True)

  @classmethod
  def poll(self, context):
      if context.object and context.object.type == 'ARMATURE' and context.active_object and context.active_object.mode == 'POSE':
          return 1
  
  count = 0
  def putButton(self, layout, icon='NONE', text=""):
      table = pitchipoyOperatorNames if isPitchipoy() else metarigOperatorNames
      if icon != 'NONE':
        layout.operator(table[self.count], icon=icon, text="")
      else:
        if text != '':
            layout.operator(table[self.count], icon=icon, text=text)
        else:
            layout.operator(table[self.count], icon=icon)

      self.count += 1

  def draw(self, context):
    l = self.layout

    #draw auto ik/fk checkbox
    l.prop(context.active_object, "is_auto_ikfk_select", text="IK/FK Auto Select Enable")

    bodyScale = 1.5
    thighHight = 6
    footHeight = 2
    handHeight = 2
    keyframeHeight = 2

    self.count = 0

#-----------------------------------------------------------------------------------------------------------------------------------------------------
# Pitchipoy
#-----------------------------------------------------------------------------------------------------------------------------------------------------
    if isPitchipoy():
        armHeight = 2.5

        #head neck chest
        row = l.row()

        row.label("")
        row.label("")

        col = row.column(align=False)
        col.alignment = 'CENTER'
        col.scale_y = 1.2
        self.putButton(col)
        subrow = col.row(align=False)
        subrow.alignment = 'CENTER'
        subrow.scale_x = 1
        self.putButton(subrow, 'WIRE')
        self.putButton(col)
        subrow = col.row(align=False)
        subrow.alignment = 'CENTER'
        subrow.scale_x = 1
        self.putButton(subrow, 'WIRE')
        self.putButton(col)

        row.label("")
        row.label("")

        #--------------------------------shoulder-----------------------------
        row = l.row()
        row.label("")

        row.operator(boneNameToOperatorName("pitchipoyArmRNames"), icon='DOWNARROW_HLT', text='ALL')

        self.putButton(row)
        self.putButton(row)

        row.operator(boneNameToOperatorName("pitchipoyArmLNames"), icon='DOWNARROW_HLT', text='ALL')

        row.label("")

        #--------------------------------arm body tweak--------------------------------
        row = l.row()
        col = row.column()

        #right arm tweak
        self.putButton(col,icon='WIRE')
        self.putButton(col,icon='WIRE')
        self.putButton(col,icon='WIRE')
        self.putButton(col,icon='WIRE')
        self.putButton(col,icon='WIRE')

        #right upper arm ik
        col = row.column()
        col.label("")
        col.label("")
        self.putButton(col,icon='WIRE')

        #right arm
        col = row.column()
        col.scale_y = armHeight
        self.putButton(col)
        self.putButton(col)

        #right breast
        col = row.column()
        self.putButton(col, icon='MESH_CIRCLE')

        #tweak
        col = row.column()
        self.putButton(col, 'WIRE')
        self.putButton(col, 'WIRE')
        self.putButton(col, 'WIRE')
        self.putButton(col, 'WIRE')

        #left breast
        col = row.column()
        self.putButton(col, icon='MESH_CIRCLE')

        #left arm
        col = row.column()
        col.scale_y = armHeight
        self.putButton(col)
        self.putButton(col)

        #left upper arm ik
        col = row.column()
        col.label("")
        col.label("")
        self.putButton(col,icon='WIRE')

        #left arm tweak
        col = row.column()
        self.putButton(col,icon='WIRE')
        self.putButton(col,icon='WIRE')
        self.putButton(col,icon='WIRE')
        self.putButton(col,icon='WIRE')
        self.putButton(col,icon='WIRE')

        #---------------------------------hips torso hand finger--------------------------------
        row = l.row()
        #right hand
        col = row.column()
        self.putButton(col)
        subrow = col.row()
        subrow.scale_y = 2
        self.putButton(subrow)
        self.putButton(subrow)

        #right finger
        subrow = col.row()
        subcol = subrow.column()
        self.putButton(subcol,text='P')
        self.putButton(subcol,text='P')
        self.putButton(subcol,text='P')
        subcol = subrow.column()
        self.putButton(subcol,text='R')
        self.putButton(subcol,text='R')
        self.putButton(subcol,text='R')
        subcol = subrow.column()
        self.putButton(subcol,text='M')
        self.putButton(subcol,text='M')
        self.putButton(subcol,text='M')
        subcol = subrow.column()
        self.putButton(subcol,text='I')
        self.putButton(subcol,text='I')
        self.putButton(subcol,text='I')
        subcol = subrow.column()
        self.putButton(subcol,text='T')
        self.putButton(subcol,text='T')
        self.putButton(subcol,text='T')

        #hip torso
        col = row.column()
        col.scale_y = 3
        self.putButton(col)
        self.putButton(col)

        #left hand
        col = row.column()
        self.putButton(col)
        subrow = col.row()
        subrow.scale_y = 2
        self.putButton(subrow)
        self.putButton(subrow)

        #left finger
        subrow = col.row()
        subcol = subrow.column()
        self.putButton(subcol,text='T')
        self.putButton(subcol,text='T')
        self.putButton(subcol,text='T')
        subcol = subrow.column()
        self.putButton(subcol,text='I')
        self.putButton(subcol,text='I')
        self.putButton(subcol,text='I')
        subcol = subrow.column()
        self.putButton(subcol,text='M')
        self.putButton(subcol,text='M')
        self.putButton(subcol,text='M')
        subcol = subrow.column()
        self.putButton(subcol,text='R')
        self.putButton(subcol,text='R')
        self.putButton(subcol,text='R')
        subcol = subrow.column()
        self.putButton(subcol,text='P')
        self.putButton(subcol,text='P')
        self.putButton(subcol,text='P')

        #------------------------------------legs-----------------------------
        row = l.row()

        row.operator(boneNameToOperatorName("pitchipoyLegRNames"), icon='TRIA_RIGHT', text='ALL')

        #left tweak
        col = row.column()
        self.putButton(col,icon='WIRE')
        self.putButton(col,icon='WIRE')
        self.putButton(col,icon='WIRE')
        self.putButton(col,icon='WIRE')
        self.putButton(col,icon='WIRE')

        #thigh ik R
        col = row.column()
        col.label("")
        col.label("")
        self.putButton(col,icon='WIRE')

        #left legs
        col = row.column()
        col.scale_y = armHeight
        self.putButton(col)
        self.putButton(col)

        #right legs
        col = row.column()
        col.scale_y = armHeight
        self.putButton(col)
        self.putButton(col)

        #thigh ik L
        col = row.column()
        col.label("")
        col.label("")
        self.putButton(col,icon='WIRE')

        #right tweak
        col = row.column()
        self.putButton(col,icon='WIRE')
        self.putButton(col,icon='WIRE')
        self.putButton(col,icon='WIRE')
        self.putButton(col,icon='WIRE')
        self.putButton(col,icon='WIRE')

        row.operator(boneNameToOperatorName("pitchipoyLegLNames"), icon='TRIA_LEFT', text='ALL')

        #-----------------------------------foot ik/fk------------------------------
        row = l.row()
        row.label("")
        row.scale_y = 2
        self.putButton(row)
        self.putButton(row)
        self.putButton(row)
        self.putButton(row)
        row.label("")

        #-----------------------------------toe heel---------------------------------
        row = l.row()
        self.putButton(row)
        self.putButton(row)
        self.putButton(row)
        self.putButton(row)

        #------------------------------------root---------------------------------------
        row = l.row()
        col = row.column()
        col.separator()
        self.putButton(col)

        #------------------------------------keyframe all--------------------------------
        col = l.column()
        col.separator()
        col.separator()
        row = col.row()
        row.scale_y = keyframeHeight
        row.label("")
        row.operator(boneNameToOperatorName("pitchipoyAllBoneNames"), text='KEYFRAME ALL')
        row.label("")

#-----------------------------------------------------------------------------------------------------------------------------------------------------
# metarig
#-----------------------------------------------------------------------------------------------------------------------------------------------------
    else:
        #head neck
        row = l.row()

        row.label("")
        row.label("")

        col = row.column()
        col.scale_y = 2
        self.putButton(col)
        self.putButton(col)

        row.label("")
        row.label("")


        #shoulder
        row = l.row()
        row.label("")

        row.operator(boneNameToOperatorName("metarigArmRNames"), icon='DOWNARROW_HLT', text='ALL')

        self.putButton(row)
        self.putButton(row)

        row.operator(boneNameToOperatorName("metarigArmLNames"), icon='DOWNARROW_HLT', text='ALL')

        row.label("")


        #---------------------------arm torso elbow tweak----------------------------------
        row = l.row()

        #right arm tweak
        col = row.column()
        self.putButton(col,'WIRE')
        self.putButton(col,'WIRE')
        self.putButton(col,'WIRE')
        self.putButton(col,'WIRE')
        self.putButton(col,'WIRE')

        #elbow pole target right
        col = row.column()
        col.label("")
        col.label("")
        self.putButton(col,'WIRE')

        #right arm
        col = row.column()
        col.scale_y = bodyScale*2
        self.putButton(col)
        self.putButton(col)

        #body
        col = row.column()
        col.scale_y = bodyScale
        self.putButton(col)
        self.putButton(col)
        self.putButton(col)
        self.putButton(col)

        #left arm
        col = row.column()
        col.scale_y = bodyScale*2
        self.putButton(col)
        self.putButton(col)

        #elbow pole target left
        col = row.column()
        col.label("")
        col.label("")
        self.putButton(col,'WIRE')

        #right arm tweak
        col = row.column()
        self.putButton(col,'WIRE')
        self.putButton(col,'WIRE')
        self.putButton(col,'WIRE')
        self.putButton(col,'WIRE')
        self.putButton(col,'WIRE')

        #--------------------thigh hand ik/fk finger----------------------------
        topRow = l.row()

        col = topRow.column()
        #right palm
        row = col.row()
        self.putButton(row)

        #right hand
        row = col.row()
        row.scale_y = handHeight
        self.putButton(row)
        self.putButton(row)

        #right finger
        row = col.row()
        self.putButton(row,text='P')
        self.putButton(row,text='R')
        self.putButton(row,text='M')
        self.putButton(row,text='I')
        self.putButton(row,text='T')

        col = topRow.column()

        #right thigh
        col.scale_y = thighHight
        self.putButton(col)

        #left thigh
        col = topRow.column()
        col.scale_y = thighHight
        self.putButton(col)

        col = topRow.column()

        #left palm
        row = col.row()
        self.putButton(row)

        #left hand
        row = col.row()
        row.scale_y = handHeight
        self.putButton(row)
        self.putButton(row)

        #right finger
        row = col.row()
        self.putButton(row,text='T')
        self.putButton(row,text='I')
        self.putButton(row,text='M')
        self.putButton(row,text='R')
        self.putButton(row,text='P')

        #---------------------------- shin pole target tweak------------------------------
        row = l.row()

        row.operator(boneNameToOperatorName("metarigLegRNames"), icon='TRIA_RIGHT', text='ALL')
        #right tweak

        col = row.column()
        self.putButton(col,'WIRE')
        self.putButton(col,'WIRE')
        self.putButton(col,'WIRE')
        self.putButton(col,'WIRE')
        self.putButton(col,'WIRE')

        row.separator()

        #right pole target
        col = row.column()
        self.putButton(col,'WIRE')

        #right shin
        col = row.column()
        col.scale_y = thighHight
        self.putButton(col)

        #left shin
        col = row.column()
        col.scale_y = thighHight
        self.putButton(col)

        #right pole target
        col = row.column()
        self.putButton(col,'WIRE')

        row.separator()

        #left tweak
        col = row.column()
        self.putButton(col,'WIRE')
        self.putButton(col,'WIRE')
        self.putButton(col,'WIRE')
        self.putButton(col,'WIRE')
        self.putButton(col,'WIRE')

        row.operator(boneNameToOperatorName("metarigLegLNames"), icon='TRIA_LEFT', text='ALL')

        #-----------------------------foot ik/fk--------------------------------
        col = l.column()

        #right foot
        row = col.row()
        row.scale_y = footHeight
        row.label("")
        self.putButton(row)
        self.putButton(row)

        #left foot
        self.putButton(row)
        self.putButton(row)

        row.label("")

        #------------------------------toe foot roll-----------------------
        col = l.column()

        #right toe
        row = col.row()
        self.putButton(row)
        self.putButton(row)

        #left toe
        self.putButton(row)
        self.putButton(row)

        #------------------------------root-------------------------------
        col = l.column()
        col.separator()
        self.putButton(col)

        #------------------------------------keyframe all--------------------------------
        col = l.column()
        col.separator()
        col.separator()
        row = col.row()
        row.scale_y = keyframeHeight
        row.label("")
        row.operator(boneNameToOperatorName("metarigAllBoneNames"), text='KEYFRAME ALL')
        row.label("")


#------------------------------------------- Register functions -------------------------------------------------
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
