import bpy


counter = "3"
file = "4000_"+counter+".dae"
path = "C:/blndrscripts/starstruk/4000/"+file
bpy.ops.wm.collada_import(filepath=path, filter_blender=False, filter_backup=False, filter_image=False, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_btx=False, filter_collada=True, filter_folder=True, filemode=8, display_type='FILE_DEFAULTDISPLAY', import_units=False, fix_orientation=False, find_chains=False, min_chain_length=0)
