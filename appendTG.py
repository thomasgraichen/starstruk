"""Author: Thomas Graichen"""
"""www.tgraichen.de"""

import bpy

bpy.ops.wm.append(
# // + name of blend file + \\Object\\
filepath="//triangle_prim.blend\\Object\\",

# name of the object
filename="triangle",

# file path of the blend file + name of the blend file + \\Object\\
directory="C:/blndrscripts/triangle_prim.blend\\Object\\",
   
# append, don't link
link = False
)
