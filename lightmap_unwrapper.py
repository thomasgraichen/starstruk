import bpy
import time
import gc


start_time = time.time()
bpy.ops.object.select_all(action='SELECT') #select all objects
bpy.ops.object.delete(use_global=False) #delete all objects (for command window, starts with default scene!)

print("default scene deleted")
print("importing dae...")
file = "8000_dist1000_all.dae"
path = "C:/blndrscripts/starstruk/8000/"+file
bpy.ops.wm.collada_import(filepath=path, filter_blender=False, filter_backup=False, filter_image=False, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_btx=False, filter_collada=True, filter_folder=True, filemode=8, display_type='FILE_DEFAULTDISPLAY', import_units=False, fix_orientation=False, find_chains=False, min_chain_length=0)

print("import complete")

print("lightmap start...")

bpy.ops.uv.lightmap_pack(PREF_CONTEXT='ALL_FACES', PREF_PACK_IN_ONE=True, PREF_NEW_UVLAYER=False, PREF_APPLY_IMAGE=False, PREF_IMG_PX_SIZE=512, PREF_BOX_DIV=12, PREF_MARGIN_DIV=0.1)
print("lightmapping complete")
elapsed_time = time.time() - start_time
print("elapsed time: "+str(elapsed_time))
gc.collect()

#save blend
blendfilename = "C:/blndrscripts/starstruk/8000/8000_dist1000_all_uv.blend"
bpy.ops.wm.save_mainfile(filepath=blendfilename)

#save collada
dae_exportpath = "C:/blndrscripts/starstruk/8000/8000_dist1000_all_uv.dae"
bpy.ops.wm.collada_export(filepath=dae_exportpath, check_existing=True, filter_blender=False, filter_image=False, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_btx=False, filter_collada=True, filter_folder=True, filemode=8, selected=False)
