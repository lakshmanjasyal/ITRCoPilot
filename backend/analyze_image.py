from PIL import Image
import numpy as np

img = Image.open('page0.png')
arr = np.array(img)
print('shape', arr.shape, 'dtype', arr.dtype)
print('min/max', arr.min(), arr.max(), 'mean', arr.mean())
print('unique colors', len(np.unique(arr.reshape(-1, arr.shape[2]), axis=0)))
# detect if mostly white
white_ratio = np.mean(np.all(arr > 240, axis=2))
print('white ratio', white_ratio)
