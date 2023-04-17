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
        
horse = Image('horse').prepare(Lib.OPENCV)
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