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
    return name.replace('.','').replace('_','').lower()

def boneNameToOperatorName(name):
    return "dskjal."+boneNameToClassName(name)

def createButton(name):
    code = 'class '+boneNameToClassName(name)+'Button(bpy.types.Operator):\n'
    code +='  bl_idname = boneNameToOperatorName("'+name+'")\n'
    code +='  bl_label = "'+name+'"\n'
    code +='  def execute(self, context):\n'
    code +='    bpy.ops.pose.select_all(action="DESELECT")\n'
    code +='    bpy.data.objects[context.active_object.name].data.bones["'+name+'"].select = True\n'
    code +='    return{"FINISHED"}\n\n'
    return code

def isPitchipoy():
    try:
        return bpy.context.active_object.data.bones['eyes'] != None
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

#pitchipoyBoneNames = metarigBoneNames

#generate buttons
generatedButtonCode = ""
for i in metarigBoneNames:
    generatedButtonCode += createButton(i)
exec(generatedButtonCode)

#cache operator names for performance
metarigOperatorNames = []
for name in metarigBoneNames:
    metarigOperatorNames.append(boneNameToOperatorName(name))

#---------------------------------------- UI --------------------------------------------------
class UI(bpy.types.Panel):
  bl_label = "Rigify Picker"
  bl_space_type = "VIEW_3D"
  bl_region_type = "UI"

  @classmethod
  def poll(self, context):
      if context.object and context.object.type == 'ARMATURE' and context.active_object and context.active_object.mode == 'POSE':
          return 1
  
  def draw(self, context):
    if isPitchipoy():
        print("not impremented")
    else:
        bodyScale = 1.5
        armWidth = 0.3
        thighHight = 6
        footHeight = 2
        handHeight = 2

        l = self.layout
        count = 0

        #head neck
        row = l.row()

        row.label("")
        row.label("")

        row.scale_x = 6
        col = row.column()
        col.scale_y = 2
        col.operator(metarigOperatorNames[count])
        count += 1
        col.operator(metarigOperatorNames[count])
        count += 1

        row.label("")
        row.label("")


        #shoulder
        row = l.row()
        row.label("")
        row.operator(metarigOperatorNames[count])
        count += 1
        row.operator(metarigOperatorNames[count])
        count += 1
        row.label("")


        #---------------------------arm torso elbow tweak----------------------------------
        row = l.row()

        #right arm tweak
        col = row.column()
        col.operator(metarigOperatorNames[count])
        count += 1
        col.operator(metarigOperatorNames[count])
        count += 1
        col.operator(metarigOperatorNames[count])
        count += 1
        col.operator(metarigOperatorNames[count])
        count += 1
        col.operator(metarigOperatorNames[count])
        count += 1

        #elbow pole target right
        col = row.column()
        col.label("")
        col.label("")
        col.operator(metarigOperatorNames[count])
        count += 1

        #right arm
        col = row.column()
        col.scale_y = bodyScale*2
        col.scale_x = armWidth
        col.operator(metarigOperatorNames[count])
        count += 1
        col.operator(metarigOperatorNames[count])
        count += 1

        #body
        col = row.column()
        col.scale_x = 0.5
        col.scale_y = bodyScale
        col.operator(metarigOperatorNames[count])
        count += 1
        col.operator(metarigOperatorNames[count])
        count += 1
        col.operator(metarigOperatorNames[count])
        count += 1
        col.operator(metarigOperatorNames[count])
        count += 1


        #left arm
        col = row.column()
        col.scale_y = bodyScale*2
        col.scale_x = armWidth
        col.operator(metarigOperatorNames[count])
        count += 1
        col.operator(metarigOperatorNames[count])
        count += 1

        #elbow pole target left
        col = row.column()
        col.label("")
        col.label("")
        col.operator(metarigOperatorNames[count])
        count += 1

        #right arm tweak
        col = row.column()
        col.operator(metarigOperatorNames[count])
        count += 1
        col.operator(metarigOperatorNames[count])
        count += 1
        col.operator(metarigOperatorNames[count])
        count += 1
        col.operator(metarigOperatorNames[count])
        count += 1
        col.operator(metarigOperatorNames[count])
        count += 1



        #--------------------thigh hand ik/fk finger----------------------------
        topRow = l.row()

        col = topRow.column()
        #right palm
        row = col.row()
        row.operator(metarigOperatorNames[count])
        count += 1

        #right hand
        row = col.row()
        row.scale_y = handHeight
        row.operator(metarigOperatorNames[count])
        count += 1
        row.operator(metarigOperatorNames[count])
        count += 1

        #right finger
        row = col.row()
        row.operator(metarigOperatorNames[count])
        count += 1
        row.operator(metarigOperatorNames[count])
        count += 1
        row.operator(metarigOperatorNames[count])
        count += 1
        row.operator(metarigOperatorNames[count])
        count += 1
        row.operator(metarigOperatorNames[count])
        count += 1


        col = topRow.column()
        #right thigh
        col.scale_y = thighHight
        col.operator(metarigOperatorNames[count])
        count += 1

        #left thigh
        col = topRow.column()
        col.scale_y = thighHight
        col.operator(metarigOperatorNames[count])
        count += 1


        col = topRow.column()
        #left palm
        row = col.row()
        row.operator(metarigOperatorNames[count])
        count += 1

        #left hand
        row = col.row()
        row.scale_y = handHeight
        row.operator(metarigOperatorNames[count])
        count += 1
        row.operator(metarigOperatorNames[count])
        count += 1

        #right finger
        row = col.row()
        row.operator(metarigOperatorNames[count])
        count += 1
        row.operator(metarigOperatorNames[count])
        count += 1
        row.operator(metarigOperatorNames[count])
        count += 1
        row.operator(metarigOperatorNames[count])
        count += 1
        row.operator(metarigOperatorNames[count])
        count += 1


        #---------------------------- shin pole target tweak------------------------------
        row = l.row()

        #right tweak
        col = row.column()
        col.operator(metarigOperatorNames[count])
        count += 1
        col.operator(metarigOperatorNames[count])
        count += 1
        col.operator(metarigOperatorNames[count])
        count += 1
        col.operator(metarigOperatorNames[count])
        count += 1
        col.operator(metarigOperatorNames[count])
        count += 1

        #right pole target
        col = row.column()
        col.operator(metarigOperatorNames[count])
        count += 1

        #right shin
        col = row.column()
        col.scale_y = thighHight
        col.operator(metarigOperatorNames[count])
        count += 1

        #left shin
        col = row.column()
        col.scale_y = thighHight
        col.operator(metarigOperatorNames[count])
        count += 1

        #right pole target
        col = row.column()
        col.operator(metarigOperatorNames[count])
        count += 1

        #left tweak
        col = row.column()
        col.operator(metarigOperatorNames[count])
        count += 1
        col.operator(metarigOperatorNames[count])
        count += 1
        col.operator(metarigOperatorNames[count])
        count += 1
        col.operator(metarigOperatorNames[count])
        count += 1
        col.operator(metarigOperatorNames[count])
        count += 1



        #-----------------------------foot ik/fk--------------------------------
        col = l.column()

        #right foot
        row = col.row()
        row.scale_y = footHeight
        row.label("")
        row.operator(metarigOperatorNames[count])
        count += 1
        row.operator(metarigOperatorNames[count])
        count += 1


        #left foot
        row.operator(metarigOperatorNames[count])
        count += 1
        row.operator(metarigOperatorNames[count])
        count += 1

        row.label("")


        #------------------------------toe foot roll-----------------------
        col = l.column()

        #right toe
        row = col.row()
        row.operator(metarigOperatorNames[count])
        count += 1
        row.operator(metarigOperatorNames[count])
        count += 1

        #left toe
        row.operator(metarigOperatorNames[count])
        count += 1
        row.operator(metarigOperatorNames[count])
        count += 1

        #------------------------------root-------------------------------
        col = l.column()
        col.separator()
        col.operator(metarigOperatorNames[count])
        count += 1




#------------------------------------------- Register functions -------------------------------------------------
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
