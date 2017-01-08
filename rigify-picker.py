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
    "version": (1, 0),
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
    code = 'class '+boneNameToClassName(name)+'Button(bpy.types.Operator):\n'
    code +='  bl_idname = boneNameToOperatorName("'+name+'")\n'
    code +='  bl_label = "'+name+'"\n'
    code +='  def execute(self, context):\n'
    code +='    bpy.ops.pose.select_all(action="DESELECT")\n'
    code +='    o = bpy.data.objects[context.active_object.name]\n'
    code +='    o.data.bones["'+name+'"].select = True\n'

    #auto ik/fk switch
    code +='    if not context.active_object.is_auto_ikfk_snap:\n'
    code +='      return {"FINISHED"}\n'
    ikfkHeader = '    if isPitchipoy():\n      print("p")\n    else:\n'
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

def isPitchipoy():
    try:
        return bpy.context.active_object.data.bones['tweak_spine.005'] != None
    except:
        return False


#---------------------------------------- Button Generator ----------------------------------------------------
metarigBoneNames = ["head",
                    "neck",
                    "shoulder.R", "shoulder.L", 
                    "upper_arm_hose_end.R", "upper_arm_hose.R", "elbow_hose.R", "forearm_hose.R", "forearm_hose_end.R",
                    "elbow_target.ik.R", "upper_arm.fk.R", "forearm.fk.R", "chest", "spine", "torso", "hips", "upper_arm.fk.L", "forearm.fk.L", "elbow_target.ik.L",
                    "upper_arm_hose_end.L", "upper_arm_hose.L", "elbow_hose.L", "forearm_hose.L", "forearm_hose_end.L",
                    "palm.R", "hand.ik.R", "hand.fk.R",
                    "f_pinky.R", "f_ring.R", "f_middle.R", "f_index.R", "thumb.R",
                    "thigh.fk.R", "thigh.fk.L", "palm.L", "hand.fk.L", "hand.ik.L",
                    "thumb.L", "f_index.L", "f_middle.L", "f_ring.L", "f_pinky.L",
                    "thigh_hose_end.R", "thigh_hose.R", "knee_hose.R", "shin_hose.R", "shin_hose_end.R",
                    "knee_target.ik.R", "shin.fk.R","shin.fk.L", "knee_target.ik.L",
                    "thigh_hose_end.L", "thigh_hose.L", "knee_hose.L", "shin_hose.L", "shin_hose_end.L",
                    "foot.ik.R", "foot.fk.R", "foot.fk.L", "foot.ik.L",
                    "toe.R", "foot_roll.ik.R", "foot_roll.ik.L", "toe.L",
                    "root"
]

pitchipoyBoneNames = ["head", "tweak_spine.005", "neck", "tweak_spine.004", "chest",
                      "shoulder.R", "shoulder.L",
                      "upper_arm_tweak.R", "upper_arm_tweak.R.001", "forearm_tweak.R", "forearm_tweak.R.001", "hand_tweak.R",
                      "upper_arm_ik.R", "upper_arm_fk.R", "forearm_fk.R", "breast.R",
                      "tweak_spine.003", "tweak_spine.002", "tweak_spine.001", "tweak_spine",
                      "breast.L", "upper_arm_fk.L", "forearm_fk.L", "upper_arm_ik.L",
                      "upper_arm_tweak.L", "upper_arm_tweak.L.001", "forearm_tweak.L", "forearm_tweak.L.001", "hand_tweak.L",
                      "palm.R", "hand_ik.R", "hand_fk.R",
                      "f_pinky.01.R", "f_pinky.02.R", "f_pinky.03.R",
                      "f_ring.01.R", "f_ring.02.R", "f_ring.03.R",
                      "f_middle.01.R", "f_middle.02.R", "f_middle.03.R",
                      "f_index.01.R", "f_index.02.R", "f_index.03.R",
                      "thumb.01.R", "thumb.02.R", "thumb.03.R",
                      "hips", "torso",
                      "palm.L", "hand_fk.L", "hand_ik.L",
                      "thumb.01.L", "thumb.02.L", "thumb.03.L",
                      "f_index.01.L", "f_index.02.L", "f_index.03.L",
                      "f_middle.01.L", "f_middle.02.L", "f_middle.03.L",
                      "f_ring.01.L", "f_ring.02.L", "f_ring.03.L",
                      "f_pinky.01.L", "f_pinky.02.L", "f_pinky.03.L",
                      "thigh_tweak.R", "thigh_tweak.R.001", "shin_tweak.R", "shin_tweak.R.001", "foot_tweak.R",
                      "thigh_ik.R",
                      "thigh_fk.R", "shin_fk.R", "thigh_fk.L", "shin_fk.L",
                      "thigh_ik.L",
                      "thigh_tweak.L", "thigh_tweak.L.001", "shin_tweak.L", "shin_tweak.L.001", "foot_tweak.L",
                      "foot_ik.R", "foot_fk.R", "foot_fk.L", "foot_ik.L",
                      "toe.R", "foot_heel_ik.R", "foot_heel_ik.L", "toe.L",
                      "root"
]

#generate buttons
generatedButtonCode = ""
for i in metarigBoneNames:
    generatedButtonCode += createButton(i)
for i in pitchipoyBoneNames:
    generatedButtonCode += createButton(i)
exec(generatedButtonCode)

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

  bpy.types.Object.is_auto_ikfk_snap = bpy.props.BoolProperty(name="",default=True)

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
    l.prop(context.active_object, "is_auto_ikfk_snap", text="IK/FK Auto Select Enable")

    bodyScale = 1.5
    thighHight = 6
    footHeight = 2
    handHeight = 2

    self.count = 0

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
        self.putButton(row)
        self.putButton(row)
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

        #left tweak
        col = row.column()
        self.putButton(col,icon='WIRE')
        self.putButton(col,icon='WIRE')
        self.putButton(col,icon='WIRE')
        self.putButton(col,icon='WIRE')
        self.putButton(col,icon='WIRE')

        row.label("")

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

        row.label("")

        #right tweak
        col = row.column()
        self.putButton(col,icon='WIRE')
        self.putButton(col,icon='WIRE')
        self.putButton(col,icon='WIRE')
        self.putButton(col,icon='WIRE')
        self.putButton(col,icon='WIRE')

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

#-------------------------------------------------------------------------------------------
# metarig
#-------------------------------------------------------------------------------------------
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
        self.putButton(row)
        self.putButton(row)
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

        #right tweak
        col = row.column()
        self.putButton(col,'WIRE')
        self.putButton(col,'WIRE')
        self.putButton(col,'WIRE')
        self.putButton(col,'WIRE')
        self.putButton(col,'WIRE')

        row.separator()
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
        row.separator()

        #left tweak
        col = row.column()
        self.putButton(col,'WIRE')
        self.putButton(col,'WIRE')
        self.putButton(col,'WIRE')
        self.putButton(col,'WIRE')
        self.putButton(col,'WIRE')



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




#------------------------------------------- Register functions -------------------------------------------------
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
