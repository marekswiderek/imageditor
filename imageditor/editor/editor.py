import numpy as np
from PIL import Image, ImageQt
import traceback
from PyQt5 import QtGui

def open_image_as_ndarray(image_path):
	image = Image.open(image_path)
	return np.asarray(image)

def save_ndarray_as_image(image_ndarray, image_path):
	#convert numpy ndarray to PIL Image format
	image = Image.fromarray(np.uint8(image_ndarray))
	image.save(image_path)

def convert_ndarray_to_pixmap(image_ndarray):
	image = Image.fromarray(np.uint8(image_ndarray)) #convert numpy array to PIL image format
	qimage = ImageQt.ImageQt(image) #convert PIL image to ImageQt
	return QtGui.QPixmap.fromImage(qimage) #create QPixmap based on ImageQt

def rgb_to_grayscale(image_ndarray):
	#using https://en.wikipedia.org/wiki/Grayscale#Converting_color_to_grayscale formula
	#dot product is 2dim ndarray
	return np.dot(image_ndarray[:, :, :3], [0.299, 0.587, 0.114])

def negative_image(image_ndarray):
	if image_ndarray.ndim==3:
		image_ndarray[:, :, 0:2] = 255 - image_ndarray[:, :, 0:2]
		return image_ndarray
	elif image_ndarray.ndim==2:
		#TO-DO: negative 2dim array
		image_ndarray[:, :] = 255 - image_ndarray[:, :]
		return image_ndarray

def only_red_channel(image_ndarray):
	if image_ndarray.ndim==3:
		image_ndarray[:, :, (1,2)] = 0
		return image_ndarray
	elif image_ndarray.ndim==2:
		print('This filter works only with 3dim ndarrays')
		return image_ndarray 

def only_green_channel(image_ndarray):
	if image_ndarray.ndim==3:
		image_ndarray[:, :, (0,2)] = 0
		return image_ndarray
	elif image_ndarray.ndim==2:
		print('This filter works only with 3dim ndarrays')
		return image_ndarray 

def only_blue_channel(image_ndarray):
	if image_ndarray.ndim==3:
		image_ndarray[:, :, (0,1)] = 0
		return image_ndarray
	elif image_ndarray.ndim==2:
		print('This filter works only with 3dim ndarrays')
		return image_ndarray 

#function used as ufunc inside remove_rgb_above_thresholds function
def filter_rgb(a, b):
	if b == True:
		return 0
	else:
		return a

#remove rgb values from image above thresholds
def remove_rgb_above_thresholds(image_ndarray, r, g, b):
	if image_ndarray.ndim==3:
		filter_rgbs = np.frompyfunc(filter_rgb, 2, 1)
		filter_ndarray = np.zeros(image_ndarray.shape, dtype=bool)
		filter_ndarray[:, :, 0] = image_ndarray[:, :, 0] >= r
		filter_ndarray[:, :, 1] = image_ndarray[:, :, 1] >= g
		filter_ndarray[:, :, 2] = image_ndarray[:, :, 2] >= b 
		image_ndarray = filter_rgbs(image_ndarray, filter_ndarray)
		return image_ndarray
	elif image_ndarray.ndim==2:
		print('This filter works only with 3dim ndarrays')
		return image_ndarray 

if __name__ == "__main__":
	pass
