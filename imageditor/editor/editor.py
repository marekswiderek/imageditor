import numpy as np
from PIL import Image, ImageQt
import traceback
from PyQt5 import QtGui

def save_ndarray_as_image(image_ndarray, image_path):
	#convert numpy ndarray to PIL Image format
	image = Image.fromarray(np.uint8(image_ndarray))
	image.save(image_path)

def convert_pixmap_to_ndarray(pixmap):
	size = pixmap.size() #get pixmap size
	w = size.width() #get width
	h = size.height() #get height
	channels_count = 4 

	qimg = pixmap.toImage() #convert pixmap to QtImage
	byte_str = qimg.bits().asstring(w * h * channels_count) #save image as string of bytes
	try:
		return np.fromstring(byte_str, dtype=np.uint8).reshape((h,w,channels_count)) #prepare an numpy array
	except Exception:
		traceback.print_exc()

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

if __name__ == "__main__":
	pass
