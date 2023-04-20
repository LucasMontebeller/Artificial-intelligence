import os
from PIL import Image as PILImage
from PIL import ImageOps as ops
import cv2
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum, auto

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(SCRIPT_DIR, '..', 'Images')
os.chdir(SCRIPT_DIR)

class Lib(Enum):
    PIL = auto()
    OPENCV = auto()

class Image:

    def __init__(self, name):
        self.path = os.path.join(IMAGE_DIR, f'{name}.png')

    def download(self, link, name):
        if not os.path.exists(self.path):
            os.system(f'wget {link} -O {name}.png -P {IMAGE_DIR}')
        else:
            print("Já existe uma imagem com este nome !")

    def prepare(self, lib):
        if os.path.exists(self.path):
            match lib:
                case Lib.PIL:
                    image = PILImage.open(self.path)
                    image_array = np.asarray(image)
                case Lib.OPENCV:
                    image_array = cv2.imread(self.path)
                    image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)

        return image_array
    
    @staticmethod
    def cut(array, height, width, channel=None):
        new_image = array.copy()
        new_image = new_image[height[0] : height[1], width[0] : width[1]]
        if channel is None:
            return new_image
        
        return new_image[:,:, channel]
    
    @staticmethod
    def super_position(array, height, width, channel):
        new_image = array.copy()
        new_image[height[0] : height[1], width[0] : width[1]] = channel
        return new_image
    
    @staticmethod
    def flip(image, lib):
        match lib:
            case Lib.PIL:
                new_image = PILImage.open(image.path)
                new_image = ops.flip(new_image)
            case Lib.OPENCV:
                new_image = Image.prepare(image, lib)
                new_image = cv2.flip(new_image, cv2.ROTATE_90_CLOCKWISE)
        return new_image
    
    @staticmethod
    def thresholding(image_array, intersection, min_value=0, max_value=255):
        n,m = image_array.shape
        output = np.zeros((n,m), dtype=np.uint8)
        
        for i in range(n):
            for j in range(m):
                if image_array[i,j] <= intersection:
                    output[i,j] = min_value
                else:
                    output[i,j] = max_value

        return output
    
    @staticmethod
    def resize(image, height_factor, width_factor):
        image = PILImage.open(image.path)
        new_height, new_width = image.size

        new_height *= height_factor
        new_width *= width_factor
        image = image.resize((int(new_height), int(new_width)))

        return image
    
    @staticmethod
    def rotate(image, theta):
        return PILImage.open(image.path).rotate(theta)
        
# horse = Image('horse').prepare(Lib.OPENCV)
# plt.i mshow(horse)
# plt.show()

# new_horse = Image.cut(horse,[17, 158], [196, 297], 2)
# plt.imshow(new_horsb e)
# plt.show()

# new_horse = Image.super_position(horse,[100, 200], [50, 150], 170)
# plt.imshow(new_horse)
# plt.show()

# flip
# horse = Image('horse')
# new_horse = PILImage.open(horse.path) 
# new_horse = ops.flip(new_horse)
# plt.imshow(new_horse)
# plt.show()

# rotate
# horse = Image('horse')
# rotate_horse_pil = Image.flip(horse, Lib.PIL) 
# rotate_horse_opencv = Image.flip(horse, Lib.OPENCV)

# plt.subplot(1,2,1)
# plt.imshow(rotate_horse_pil)

# plt.subplot(1,2,2)
# plt.imshow(rotate_horse_opencv)

# plt.show()

# testes
# array = np.array([[0,2,2], [1,1,1], [1,1,2]], dtype=np.uint8)
# plt.imshow(array, cmap="gray")
# plt.show()
# plt.bar([x for x in range(6)], [0,0,2,3,1,0])
# plt.show()
# lista = np.zeros([2,2], dtype=np.uint8)
# lista = [x for x in range(0,6)]

# horse = Image('horse')
# new_horse = cv2.imread(horse.path, cv2.IMREAD_GRAYSCALE)
# horse = cv2.cvtColor(horse, cv2.COLOR_BGR2RGB)
# hist = cv2.calcHist([horse],[0], None, [256], [0,256])

# plt.imshow(horse)
# plt.show()
# print(horse.shape)

# intensity_values = np.array([x for x in range(hist.shape[0])])
# plt.bar(intensity_values, hist[:, 0], width=5)
# plt.show()

# PMF = hist / (horse.shape[0] * horse.shape[1])
# plt.plot(intensity_values, hist)
# plt.show()

# Transformacao -> negative images
# new_horse = -1 * horse + 255
# new_horse = cv2.convertScaleAbs(horse, alpha=-1, beta=255)
# plt.imshow(new_horse)
# plt.show()


# new_horse = Image.thresholding(new_horse, 190)
# plt.imshow(new_horse, cmap="gray")
# plt.show()


# horse = Image('horse')
# horse_size = PILImage.open(horse.path).size
# print(horse_size)
# new_horse = Image.resize(horse, 1/10, 1/20)
# print(new_horse.size)
# new_rotated_horse = Image.rotate(horse, 45)

# plt.subplot(1,2,1)
# plt.imshow(new_horse)

# plt.subplot(1,2,2)
# plt.imshow(new_rotated_horse)
# plt.show()

# noise
# horse = Image('horse')
# horse = PILImage.open(horse.path)
# horse = np.array(horse)

# Noise = np.random.normal(0, 20, (height, width, 3)).astype(np.uint8)
# Noise.shape
# # horse = horse * 20
# plt.imshow(horse)
# plt.show()


table = np.array([[1,3], [2,4]])
print(table.max(axis=1))