# Skribblify

## About
Skribblify is a simple script that converts images to the [skribbl.io](https://skribbl.io/) color palette which only uses 26 different colors.

<img src="examples\pexels-robertkso-16244387.jpg" width=360px/> <img src="examples\converted%20pexels-robertkso-16244387.jpg" width=360px/>

*Credit: [An old Rusty Van on a Rural Field - Robert So](https://www.pexels.com/photo/an-old-rusty-van-on-a-rural-field-16244387/) from [Pexels](https://www.pexels.com/hu-hu/)*

## Installation
1. Clone or download this repository
2. Open it in your preferred development environment
3. Run the following command: ```pip install -r requirements.txt```
4. You are ready :D

## Usage
The script takes all **.png**, **.jpg** and **.jpeg** files in the same directory and converts them by making copies and prefixing the filenames with *"converted "*.
You can use the ```-i```, ```-o``` and ```-p``` flags to set input and output directories and filename prefix respectively.

## Performance
Even with multithreading, the script can take quite a while to finish, possibly because of the interpreted nature of python, iterating over all pixels and all the RGB to CIELAB conversions. It took about 18 seconds for the example image (with a resolution of 1920x1421) running on a 2,9 GHz - 4,2 GHz CPU with 8 cores and 16 threads.

Improving performance and color matching are probably the two most important aspects for this project.