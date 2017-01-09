# RigifyPicker

This script is picker for Rigify. Supported Level is Testing and Categories is Rigging.

Picker is visible only in Pose Mode on Properties Shelf.

Metarig and Pitchipoy body is supported.

# How to add extra bones
##keyframe
Add your extra bone names to metarigAllBoneNames or pitchipoyAllBoneNames.
>metarigAllBoneNames   = generateFingerList(".R") + generateFingerList(".L") + metarigBoneNames + ["my_bone1", "my_bone2"]
