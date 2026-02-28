from PIL import Image
import numpy as np

img = Image.open('page0.png').convert('L')
img = img.resize((80, 100))
arr = np.array(img)
chars = " .:-=+*#%@"
for row in arr:
    line = ''.join(chars[int(val/255*(len(chars)-1))] for val in row)
    print(line)
