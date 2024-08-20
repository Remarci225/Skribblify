# ==================
# Skribblify
# ------------------
# Author: Remarci225
# ==================


# Imports
# =======
from argparse import ArgumentParser
from pathlib import Path
from os import listdir
from PIL import Image
from math import cbrt
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count


# Constants
# =========
SUPPORTED_FORMATS = ["png", "jpg", "jpeg"]

COLORS = [
    ((255, 255, 255), (100.0, 0.0019288242798509714, -0.009795878399820879)),
    ((0, 0, 0), (0.0, 0.0, 0.0)),
    ((193, 193, 193), (78.06804360790544, 0.0015641441937774836, -0.00794378548703012)),
    ((80, 80, 80), (34.02862316443873, 0.0008318657159223086, -0.004224778526118467)),
    ((239, 19, 11), (50.50022617975232, 74.75290834352649, 61.34942916415176)),
    ((116, 11, 7), (23.56433203460626, 42.58351869447127, 32.34777184120819)),
    ((255, 113, 0), (64.21775468969531, 50.02541962305684, 72.38859747427199)),
    ((194, 56, 0), (44.656850102788184, 53.08621652978424, 56.50251877487948)),
    ((255, 228, 0), (90.20494969194934, -8.446064549690435, 89.46493336189324)),
    ((232, 162, 0), (71.5525721051447, 15.744399015153675, 75.42411080881635)),
    ((0, 204, 0), (71.68084944389129, -72.84720577427306, 70.30681927414962)),
    ((0, 70, 25), (25.108133027946373, -31.20696976521603, 21.343399970244555)),
    ((0, 255, 145), (88.71617210498218, -73.97128676678655, 38.71231872367462)),
    ((0, 120, 93), (44.55141873539338, -35.73003893347959, 6.826555536129675)),
    ((0, 178, 255), (68.79527662821968, -10.666196452199127, -48.43772599769729)),
    ((0, 86, 158), (36.22232960379765, 6.938045026812056, -45.12430141662922)),
    ((35, 31, 211), (29.514279243755468, 61.04099296881776, -87.39672424350273)),
    ((14, 8, 101), (10.60606857513346, 36.29770749025354, -51.088293947049614)),
    ((163, 0, 186), (40.133616231397845, 73.92803762808725, -54.77237926445477)),
    ((85, 0, 105), (19.847453396211172, 47.79255106167757, -38.17420510403695)),
    ((223, 105, 167), (60.41017669793527, 52.86073142013259, -11.304080438825403)),
    ((135, 53, 84), (34.67549431166724, 38.28994886793446, -0.7658436719981565)),
    ((255, 172, 142), (77.708232377821, 27.075329441481333, 27.82550824892558)),
    ((204, 119, 77), (58.5712296550886, 29.41638474180103, 37.094912585289144)),
    ((160, 82, 45), (43.796139581025685, 29.324941748803845, 35.63667996216117)),
    ((99, 48, 13), (26.14434788696905, 20.426380558580703, 31.121640342598912))]

LAB_VALUES = {}

ONE_THIRD = 1 / 3
DELTA = 6 / 29
INVERSE_DELTA = 29 / 6
CUBED_DELTA = DELTA ** 3
FOUR_TWENTYNINTH = 4 / 29

XN = 95.0489
YN = 100
ZN = 108.8840


# Functions
# =========
def get_full_path(path):
    relative_markers = ['.', '/', '\\']
    stripped_path = path
    for relative_marker in relative_markers:
        stripped_path = stripped_path.lstrip(relative_marker)
        
    current_path = Path().cwd()
    new_path = current_path if path == "" else Path(current_path, stripped_path) if path[0] in relative_markers else path
    return new_path if Path(new_path).exists() else current_path

def f(t):
    return cbrt(t) if t > CUBED_DELTA else ONE_THIRD * (INVERSE_DELTA ** 2) * t + FOUR_TWENTYNINTH

def rgb_to_lab(rgb):
    R = rgb[0] / 255
    G = rgb[1] / 255
    B = rgb[2] / 255
    
    R2 = (((R + 0.055) / 1.055) ** 2.4 if R > 0.04045 else R / 12.92) * 100
    G2 = (((G + 0.055) / 1.055) ** 2.4 if G > 0.04045 else G / 12.92) * 100
    B2 = (((B + 0.055) / 1.055) ** 2.4 if B > 0.04045 else B / 12.92) * 100
    
    X = 0.4124 * R2 + 0.3576 * G2 + 0.1805 * B2
    Y = 0.2126 * R2 + 0.7152 * G2 + 0.0722 * B2
    Z = 0.0193 * R2 + 0.1192 * G2 + 0.9505 * B2
    
    L = 116 * f(Y / YN) - 16
    a = 500 * (f(X / XN) - f(Y / YN))
    b = 200 * (f(Y / YN) - f(Z / ZN))
    
    return (L, a, b)

def get_difference(values, new_values):
    if values in LAB_VALUES:
        lab_values = LAB_VALUES[values]
    else:
        lab_values = rgb_to_lab(values)
        LAB_VALUES[values] = lab_values
    return (
        lab_values[0] - new_values[0]) ** 2 + (lab_values[1] - new_values[1]) ** 2 + (lab_values[2] - new_values[2]) ** 2
    
def change_pixel(x_start, x_count):
    for x in range(x_start, x_start + x_count):
        for y in range(height):
            pixel = pixels[x, y]
            min_index = 0
            min_difference = get_difference(pixel, COLORS[min_index][1])

            for k in range(1, len(COLORS)):
                difference = get_difference(pixel, COLORS[k][1])
                if difference < min_difference:
                    min_index = k
                    min_difference = difference

            pixels[x, y] = COLORS[min_index][0]


# Operations
# ==========
parser = ArgumentParser(
    prog="Skribblify",
    description="Convert images to the skribbl.io color palette"
)

parser.add_argument("-i", type=str, action="store", dest="input", default="", required=False,
                    help="input path for images, current directory by default")
parser.add_argument("-o", type=str, action="store", dest="output", default="", required=False,
                    help="output path for images, current directory by default")
parser.add_argument("-p", type=str, action="store", dest="prefix", default="converted ", required=False,
                    help="prefix for the generated image filenames, \"converted \" by default")
arguments = parser.parse_args()

input_path = get_full_path(arguments.input)
output_path = get_full_path(arguments.output)
prefix = arguments.prefix


files = listdir(input_path)
image_files = [file for file in files if file.split('.')[-1] in SUPPORTED_FORMATS and file[:9] != "converted"]

print("Starting skribblifying...")

for image_file in image_files:
    print(f"Skribblifying {image_file}...")
    
    image = Image.open(image_file)
    pixels = image.load()
    width, height = image.size
    
    thread_count = cpu_count() * 2
    threadPoolExecutor = ThreadPoolExecutor(thread_count)
    
    x_count = int(width / thread_count)
    last_x_count = x_count + width - thread_count * x_count

    
    for x in range(thread_count - 1):
        threadPoolExecutor.submit(change_pixel, x * x_count, x_count)
    threadPoolExecutor.submit(change_pixel, width - last_x_count, last_x_count)
    
    threadPoolExecutor.shutdown()
    
    image.save(f"{Path(output_path, f'{prefix}{image_file}')}")

print("Skribblifying Done! :D")