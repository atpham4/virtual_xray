import matplotlib.pyplot as plt
import numpy as np
import math
import mpl_toolkits.mplot3d.axes3d as axes3d
import scipy.misc
from scipy import ndimage
from scipy.interpolate import spline
from mpl_toolkits.mplot3d import Axes3D
from scipy.ndimage import generic_filter, correlate, minimum_filter

#Function to calculate intensities of the x-ray when passing through a slice of tissues
def intensity_function(Io, xray):
    Istart = Io
    L = len(xray[0])
    Ifilm = []
    for j in xray:
        layerposition = 0
        for k in j:
            layerposition += 1
            I = Io * math.exp(-k * L)
            Io = I
            if layerposition == len(j):
                Ifilm.append(I)
        Io = Istart
    return Ifilm

#Line Graph of Intensities for each slice
def intensity_line_graph(intensityList, Io):
    plt.figure(4)
    plt.title("Intensity Line Graph")
    x = range(len(intensityList))
    y = intensityList
    plt.plot(x, y)
    plt.axis([0, len(intensityList), 0, Io])
    plt.xlabel("Rays")
    plt.ylabel("Intensity")

#Function to generate and show 2D Phantom based on input tissue with length and angle 
def generate_2d_phantom(tissue_array, length, angle):
	if angle != 90:
		percent = 7-(7*(angle/90)) 
	else:
		percent = 0 

	plt.figure(1)
	plt.title("Phantom 2-D")
	#x 0-6, y 7-0
	if length == 6:
		plt.imshow(tissue_array, cmap= "gray")
		
	elif length == 5:
		plt.xlim(0.5, 5.5)
		plt.ylim(7 - percent - .5, percent)
		blur_img = ndimage.gaussian_filter(tissue_array, sigma = .4)
		plt.imshow(tissue_array, cmap= "gray")

	elif length == 4:
		plt.xlim(.8, 5.2)
		plt.ylim(7 - percent -.8, percent + .3)
		blur_img = ndimage.gaussian_filter(tissue_array, sigma = .4)
		plt.imshow(tissue_array, cmap= "gray")

	elif length == 3:
		plt.xlim([1, 5])
		plt.ylim([6 - percent - .5, 1 + percent])
		blur_img = ndimage.gaussian_filter(tissue_array, sigma = .4)
		plt.imshow(blur_img, cmap="gray")

	elif length == 2:
		plt.xlim([1.5, 4.5])
		plt.ylim([5.5 - percent, 1.5 + percent])
		blur_img = ndimage.gaussian_filter(tissue_array, sigma = .5)
		plt.imshow(blur_img, cmap="gray")

	elif length == 1:
		plt.xlim([2, 4])
		plt.ylim([5 - percent, 2 + percent])
		blur_img = ndimage.gaussian_filter(tissue_array, sigma = .6)
		plt.imshow(blur_img, cmap="gray")

	elif length == 0:
		plt.xlim([2.5, 3.5])
		plt.ylim([4.5 - percent, 2.5 + percent])
		blur_img = ndimage.gaussian_filter(tissue_array, sigma = .7)
		plt.imshow(blur_img, cmap="gray")

#Function to generate 3D phantom of leg
def generate_3d_phantom(skin_array, bone_array):
	fig = plt.figure(2)
	ax = fig.add_subplot(111, projection = '3d')

	data = np.array(skin_array)
	h, w = data.shape
	theta, z = np.linspace(0, 2 * np.pi, w), np.linspace(0, 1, h)
	THETA, Z = np.meshgrid(theta, z)
	X = np.cos(THETA)
	Y = np.sin(THETA)

	cmap = plt.get_cmap('gray_r')
	ax.plot_surface(
    	X, Y, Z, rstride = 1, cstride = 1, facecolors = cmap(data),
    	linewidth = 0, antialiased = False, alpha = 0.75)

	X = [element/2 for element in X]
	Y = [element/2 for element in Y]

	data = np.array(bone_array);
	cmap =plt.get_cmap('Blues')
	ax.plot_surface(
		X, Y, Z, rstride = 1, cstride = 1, facecolors = cmap(data),
		linewidth = 0, antialiased = False, alpha = 0.75)

#Function to generate tissue of the leg for 2d phantom
def generate_tissue(u_leg, u_bone):
	tissue = np.array([[u_leg, u_leg, u_bone, u_bone, u_bone, u_leg, u_leg], [u_leg, u_leg, u_bone, u_bone, u_leg, u_leg, u_leg], [u_leg, u_leg, u_bone, u_leg, u_leg, u_leg, u_leg], [u_leg, u_leg, u_leg, u_leg, u_leg, u_leg, u_leg], [u_leg, u_leg, u_leg, u_leg, u_bone, u_leg, u_leg], [u_leg, u_leg, u_leg, u_bone, u_bone, u_leg, u_leg], [u_leg, u_leg, u_bone, u_bone, u_bone, u_leg, u_leg], [u_leg, u_leg, u_bone, u_bone, u_bone, u_leg, u_leg]])
	return tissue

#Function to generate a healthy phantom of leg
def generate_leg(u_leg, u_bone):
	skin = [[u_leg]*20]*19
	bone_3d = [[u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone]]*19
	return skin, bone_3d

#Function to generate a broken leg with two splits to represent breaks in the leg
def generate_broken_leg(u_leg, u_bone):
	skin = [[u_leg]*20]*19
	bone_3d = [[u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone],
	[u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone],
	[u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone],
	[u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, 0, 0, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone],
	[u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, 0, 0, 0, 0, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone],
	[u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, 0, 0, u_bone, u_bone, 0, 0, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone],
	[u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, 0, 0, u_bone, u_bone, u_bone, u_bone, 0, 0, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone],
	[u_bone, u_bone, u_bone, u_bone, u_bone, 0, 0, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, 0, 0, u_bone, u_bone, u_bone, u_bone, u_bone],
	[u_bone, u_bone, u_bone, u_bone, 0, 0, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, 0, 0, u_bone, u_bone, u_bone, u_bone],
	[u_bone, u_bone, u_bone, 0, 0, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, 0, 0, u_bone, u_bone, u_bone],
	[u_bone, u_bone, 0, 0, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, 0, 0, u_bone, u_bone],
	[u_bone, 0, 0, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, 0, 0, u_bone],
	[0, 0, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, 0, 0],
	[0, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, 0],
	[u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone],
	[u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone]]
	return skin, bone_3d

#Function that generate a broken leg with a bigger diagonal split for observation
def generate_bigger_broken_leg(u_leg, u_bone):
	skin = [[u_leg]*20]*19
	bone_3d = [[u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone],
	[u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone],
	[u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone],
	[u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, 0, 0, 0, 0, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone],
	[u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, 0, 0, 0, 0, 0, 0, 0, 0, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone],
	[u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, 0, 0, 0, 0, 0, 0, 0, 0, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone],
	[u_bone, u_bone, u_bone, u_bone, u_bone, 0, 0, 0, 0, u_bone, u_bone, 0, 0, 0, 0, u_bone, u_bone, u_bone, u_bone, u_bone],
	[u_bone, u_bone, u_bone, u_bone, 0, 0, 0, 0, u_bone, u_bone, u_bone, u_bone, 0, 0, 0, 0, u_bone, u_bone, u_bone, u_bone],
	[u_bone, u_bone, u_bone, 0, 0, 0, 0, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, 0, 0, 0, 0, u_bone, u_bone, u_bone],
	[u_bone, u_bone, 0, 0, 0, 0, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, 0, 0, 0, 0, u_bone, u_bone],
	[u_bone, 0, 0, 0, 0, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, 0, 0, 0, 0, u_bone],
	[0, 0, 0, 0, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, 0, 0, 0, 0],
	[0, 0, 0, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, 0, 0, 0],
	[0, 0, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, 0, 0],
	[u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone],
	[u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone, u_bone]]
	return skin, bone_3d

#Calculating the density based on the inputted energy and the intensities 
def calculate_density(intensity_array, xray_energy):
	densities = []
	for intensity in intensity_array:
		densities.append(math.log(xray_energy/intensity))
	return densities

#Getting 1D image from a 2D phantom to represent density of the film
def get_1d_profile(xray_energy, tissue):
	intensities = intensity_function(xray_energy, tissue)
	density = calculate_density(intensities, xray_energy)
	plt.figure(1)
	x = range(len(density))
	y = density

	plt.plot(x, y, 'o', x, y)

#Getting the 2D image from the 3D phantom to represent the x-ray film
def get_2d_profile(xray_energy, leg, length, angle, leg_view):
	if angle != 90:
		percent = 18 - (18 * (angle / 90)) 
	else:
		percent = 0 

	intensities = []
	density = []
	
	for i in range(int(len(leg[0][0]) - 1)):
		leg_and_bone = get_2d_leg(leg[1][i], leg[0][2][0])

		if leg_view == "Side": 
			array_axis = len(leg_and_bone[0])
			leg_and_bone = np.rot90(leg_and_bone, 1, axes = (0, 1))
		intensities.append(intensity_function(xray_energy, leg_and_bone))

	for intensity in intensities:
		density.append(calculate_density(intensity, xray_energy))

	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_title('film')
	ax.set_aspect('equal')
	
	#x is from 0-8, y is 18-0
	if length == 6: 
		ax.set_ylim(18 - percent, 0  + percent)
		plt.imshow(np.array(density), cmap = plt.get_cmap('gray'))

	elif length == 5:
		ax.set_xlim(0.5, 7.5)
		ax.set_ylim(18 - percent - 1, 0.5 + percent)
		blur_img = ndimage.gaussian_filter(np.array(density), sigma = .4)
		plt.imshow(blur_img, cmap="gray")

	elif length == 4:
		ax.set_xlim(1, 7)
		ax.set_ylim(17 - percent - 1, 1.5 + percent)
		blur_img = ndimage.gaussian_filter(np.array(density), sigma = .5)
		plt.imshow(blur_img, cmap="gray")

	elif length == 3:
		ax.set_xlim(1.5, 6.5)
		ax.set_ylim(16 - percent - 1, 2 + percent)
		blur_img = ndimage.gaussian_filter(np.array(density), sigma = .6)
		plt.imshow(blur_img, cmap="gray")

	elif length == 2:
		ax.set_xlim(2, 6)
		ax.set_ylim(15 - percent - 1, 2.5 + percent)
		blur_img = ndimage.gaussian_filter(np.array(density), sigma = .7)
		plt.imshow(blur_img, cmap="gray")

	elif length == 1:
		ax.set_xlim(2.5, 5.5)
		ax.set_ylim(14 - percent - 1, 3 + percent)
		blur_img = ndimage.gaussian_filter(np.array(density), sigma = .8)
		plt.imshow(blur_img, cmap="gray")

	elif length == 0:
		ax.set_xlim(3, 5	)
		ax.set_ylim(15 - percent - 1, 3.5 + percent)
		blur_img = ndimage.gaussian_filter(np.array(density), sigma = .9)
		plt.imshow(blur_img, cmap="gray")

	cax = fig.add_axes([0.24, 0.1, 0.78, 0.8])
	cax.get_xaxis().set_visible(False)
	cax.get_yaxis().set_visible(False)
	cax.patch.set_alpha(0)
	cax.set_frame_on(False)
	plt.colorbar(orientation='vertical', pad = 0.15)

#Getting slices of tissues from the leg to get the intensities of the entire leg
def get_2d_leg(array, skin_u):
	leg_2d = []
	end_index = int(len(array)/2)
	for i in range(int(len(array)/4)):
		new_array = array[i : end_index]
		end_index -= 1

		new_array.append(skin_u)
		new_array.insert(0, skin_u)

		if i != 0:
	  		for skin in range(i):
	  			new_array.append(0)
	  			new_array.insert(0, 0)
		leg_2d.insert(0, new_array)

	start_index = int(len(array)/2)
	end_index = int(len(array))

	for i in range(int(len(array)/4)):
		new_array = array[start_index : end_index]
		new_array.reverse()
		start_index += 1
		end_index -= 1

		new_array.append(skin_u)
		new_array.insert(0, skin_u)

		if i != 0:
			for skin in range(i):
				new_array.append(0)
				new_array.insert(0, 0)
		leg_2d.append(new_array)
	array = np.array(leg_2d)
	return(array)
