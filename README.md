# RigifyPicker

This script is picker for Rigify. Supported Level is Testing and Categories is Rigging.

Picker is visible only in Pose Mode on Properties Shelf.

Metarig and Pitchipoy body/face is supported.

# How to add extra bones
##picker

1. Add your extra bone name to metarigBoneNames or pitchipoyBoneNames.
2. Update metarig[(Arm)|(Leg)][LR]Names or pitchipoy[(Arm)|(Leg)][LR]Names index.
3. Add self.putButton to correspondent location.

##keyframe
Add your extra bone names to metarigAllBoneNames or pitchipoyAllBoneNames.

```python:rigify-picker.py
metarigAllBoneNames = generateFingerList(".R") + generateFingerList(".L") + metarigBoneNames + ["my_bone1", "my_bone2"]
```
