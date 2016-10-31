"""Author: Thomas Graichen"""
"""www.tgraichen.de"""

import bpy
import numpy
import csv
import gc
import sys
import time
import winsound



#define function: bv to rgb (floats)
def bv_to_rgb(bv):
	# bv to kelvin (t)
	t = 4600 * ((1 / ((0.92 * bv) + 1.7)) +(1 / ((0.92 * bv) + 0.62)) );
	
	# kelvin (t) to xyY
	x = 0
	y = 0
	# x...
	if (t >= 1667 and t <= 4000):
		x = ((-0.2661239 * 10**9) / t**3) + ((-0.2343580 * 10**6) / t**2) + (0.8776956 * 10**3) / t + 0.179910
	elif (t > 4000 and t <= 25000):
		x = ((-3.0258469 * 10**9) / t**3) + ((2.1070379 * 10**6) / t**2) + (0.2226347 * 10**3) / t + 0.240390
	# y...
	if (t >= 1667 and t <= 2222):
		y = -1.1063814 * x**3 - 1.34811020 * x**2 + 2.18555832 * x - 0.20219683
	elif (t > 2222 and t <= 4000):
		y = -0.9549476 * x**3 - 1.37418593 * x**2 + 2.09137015 * x - 0.16748867
	elif (t > 4000 and t <= 25000):
		 y = 3.0817580 * x**3 - 5.87338670 * x**2 + 3.75112997 * x - 0.37001483
		 
	# xyY to XYZ, Y = 1
	Y = 1.0
	if (y!=0): 
		Y = 1
		X = (x*Y)/y
		Z = ((1-x-y)*Y)/y
	else:
		Y = 1
		X = (x*Y)
		Z = ((1-x-y)*Y)
		
	# XYZ to RGB
	r = 3.2406 * X - 1.5372 * Y - 0.4986 * Z
	g = -0.9689 * X + 1.8758 * Y + 0.0415 * Z
	b = 0.0557 * X - 0.2040 * Y + 1.0570 * Z
	
	# RGB to sRGB (.../255 -> floats 0-1)
	a = 0.055
	if (r <= 0.0031308):
		R = (12.92*r)/255
	elif (r > 0.0031308):
		R =  (((1+a)*r**(1/2.4))-a)#/255
	if (g <= 0.0031308):
		G = (12.92*g)/255
	elif (g > 0.0031308):
		G =  (((1+a)*g**(1/2.4))-a)#/255
	if (b <= 0.0031308):
		B = (12.92*b)/255
	elif (b > 0.0031308):
		B =  (((1+a)*b**(1/2.4))-a)#/255
	
	
	
	return (R, G, B);

#define function: color vertices of active vertex_colors
def color_vertex(obj, color):
	"""
	Paints all vertices where vert is the index of the vertex
	and color is a tuple with the RGB values (floats 0-1).
	example usage:
	color = (1.0, 0.0, 1.0)  # pink
	color_vertex(bpy.context.scene.objects['star'], 1, color)
	"""
	
	mesh = obj.data
	scn = bpy.context.scene
	
	#we need to make sure it's the active object
	scn.objects.active = obj
	obj.select = True
	vcol_layer = mesh.vertex_colors.active
	for poly in mesh.polygons:
		for loop_index in poly.loop_indices:
			loop_vert_index = mesh.loops[loop_index].vertex_index
			vcol_layer.data[loop_index].color = color
	
	return 0



xp=[-1,15]
fp=[1,0]
iterator = 0
starcount = 0



csvfrag_size = "8000"
csvfrag_num = "11"
csvfrag_name = "C:/blndrscripts/starstruk/"+csvfrag_size+"/hygfull_processed_refined_2_"+csvfrag_num+".csv"

dist = 1000 #star's distance to center


bpy.ops.object.select_all(action='SELECT') #select all objects
bpy.ops.object.delete(use_global=False) #delete all objects (for command window, starts with default scene!)


#get values from csv and store in seperate vars
with open(csvfrag_name, newline ='') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=',')
	for row in csvreader:
		
		start_time = time.time()
		
		iterator += 1
		RA_str = row[2]
		DE_str = row[3]
		mag_str = row[4]
		bv_str = row[5]
		planerot = 90 * 0.0174532925
		
		try:
			RA = (float(RA_str))*(15)*0.0174532925 #convert to deg (*15), convert to radians (*0.0174532925)
			DE = float(DE_str)*0.0174532925 #convert to radians (*0.0174532925)
		except:
			continue
		try:
			mag_float = float(mag_str)
			if (-5<=mag_float<=15):
				mag = numpy.interp(mag_float,xp,fp)
			else:
				continue
		except:
			mag = numpy.interp(7.9,xp,fp)
		try:
			bv_float = float(bv_str)
			if (-0.5<=bv_float<=9):
				bv = bv_float
			else:
				continue
		except:
			bv = 0.73
		
		
		#import triangle
		bpy.ops.wm.append(filepath="//triangle_prim.blend\\Object\\",filename="triangle",directory="C:/blndrscripts/triangle_prim.blend\\Object\\",link = False)
		#rename triangle to star...
		triangle = bpy.data.objects['triangle']
		triangle.name = 'star'+'_'+str(iterator)
		bpy.ops.object.select_all(action='DESELECT') #deselect all object
		bpy.data.objects['star'+'_'+str(iterator)].select = True #select star
		bpy.context.scene.objects.active = bpy.data.objects['star'+'_'+str(iterator)] #set star active
		
		#add vertex color layer (color)
		bpy.ops.mesh.vertex_color_add()
		#bv -> rgb, save tuple in variable 'color'
		color = bv_to_rgb(bv)
		#paint active layer with values from tupel 'color'
		color_vertex(bpy.context.scene.objects['star'+'_'+str(iterator)], color)

		#scale object according to magnitude)
		bpy.ops.transform.resize(value=(mag, mag, mag), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, snap=False, snap_target='CLOSEST', snap_point=(0, 0, 0), snap_align=False, snap_normal=(0, 0, 0), gpencil_strokes=False, texture_space=False, remove_on_cancel=False, release_confirm=False)
		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
		
		# rotate active items (here: star; value in radians; aktive Axen auf 1 stellen, x y z)
		bpy.ops.transform.rotate(value=planerot, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
		# move selected item (here: star) "dist" (s.a.) units up y-axis
		bpy.ops.transform.translate(value=(0, dist, 0), constraint_axis=(False, True, False), constraint_orientation='LOCAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
		# Apply the object's transformation to its data
		bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
		
		#rotate star on x-axis (Declination) (global)
		bpy.ops.transform.rotate(value=DE, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
		#rotate star on z-axis (Right Acsension) (global)
		bpy.ops.transform.rotate(value=RA, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
		#apply rotations
		bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

		#select and merge all objects
		bpy.ops.object.select_all(action='SELECT') # select all
		bpy.context.scene.objects.active = bpy.data.objects['star'+'_'+str(iterator)] #set active
		bpy.ops.object.join()
		bpy.ops.object.select_all(action='DESELECT') # deselect all, hier inaktiv wg export unten
		
		starcount += 1
		print("starcount: "+str(starcount))


#how much time did it take?
end_time = time.time()
time_taken = end_time - start_time
#how many rows were accessed?
print("accessed rows: "+str(iterator))
#how many stars were drawn?
print("stars drawn: "+str(starcount))


#garbage collection
csvreader = 0
csvfile = 0
gc.collect()


#save blend
blendfilename = "C:/blndrscripts/starstruk/"+csvfrag_size+"/"+ csvfrag_size + "_" + "dist" + str(dist) + "_" +csvfrag_num+".blend"
bpy.ops.wm.save_mainfile(filepath=blendfilename)

#save collada
dae_exportpath = "C:/blndrscripts/starstruk/"+csvfrag_size+"/"+ csvfrag_size + "_" + "dist" + str(dist) + "_" +csvfrag_num+".dae"
bpy.ops.wm.collada_export(filepath=dae_exportpath, check_existing=True, filter_blender=False, filter_image=False, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_btx=False, filter_collada=True, filter_folder=True, filemode=8, selected=False)

# Play Windows exit sound.
winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
tt = time.localtime(time_taken)
tt_hms = (tt[3],tt[4],tt[5])
print("time taken : " + str(tt_hms))
