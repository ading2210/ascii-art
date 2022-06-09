## Braille ASCII Art Generator:

This program is can take any bitmap image and turn it into text that is comprised of braille unicode symbols. It supports dithering, inverting the image, custom sizes and scaling options, and a custom threshold if dithering is off. 

### Usage from the command line:

```
allen@debian-pc:~/Documents/python/ascii-art$ python3 ascii.py --help
usage: ascii.py [-h] [-d] [-n] [-s SCALE] [-t THRESHOLD] [-y SIZEY] [-x SIZEX] path

Convert images to braille unicode characters.

positional arguments:
  path                  The path to the image that you want to convert.

optional arguments:
  -h, --help            show this help message and exit
  -d, --dithering       Enable dithering.
  -n, --negative        Invert the image before coverting.
  -s SCALE, --scale SCALE
                        Scale the image by this amount. If this is set the program will ignore SIZEX and SIZEY.
  -t THRESHOLD, --threshold THRESHOLD
                        Any pixels over this value will be recorded as white, any below will be recorded as black. This option does nothing if dithering is enabled. Values range from 1-255.
  -y SIZEY, --sizey SIZEY
                        Resize the image to this height before converting it. SIZEX also has to be set for this to do anything.
  -x SIZEX, --sizex SIZEX
                        Resize the image to this width. Keep in mind that each character is 2x4 pixels.
```

### Usage as a Python module:

```python
import ascii

result = ascii.convert_image("samples/dithering_test.png")
#returns a string

#additional arguments:
#dithering (bool) - Enable or disable dithering.
#negative (bool) - Invert the image.
#scale (float) - Scale the image by this amount.
#size (tuple) - Resize the image to this size.
#threshold (int) - The threshold to use if dithering is disabled.

print(results)
```
