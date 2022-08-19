import numpy as np
from PIL import Image

def open_image_as_ndarray(image_path):
	try:
		with Image.open(image_path) as image:
			return np.asarray(image)
	except Exception:
		print("ERROR")
		return Null
	#image = Image.open(image_path)
	#return np.asarray(image)

def ndarray_to_image(image_ndarray):
	if isinstance(image_ndarray, np.ndarray):
		return Image.fromarray(np.uint8(image_ndarray))
	else:
		return Null

if __name__ == "__main__":
	pass
