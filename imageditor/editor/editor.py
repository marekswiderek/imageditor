import numpy as np
from PIL import Image
import traceback

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

if __name__ == "__main__":
	pass
