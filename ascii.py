from PIL import Image, ImageOps
import argparse

def convert_image(path, dithering=False, threshold=128, negative=False, size=None, scale=1):
    img = Image.open(path).convert("L")
    if size != None:
        img = img.resize(size)
    elif scale != 1:
        width, height = img.size
        img = img.resize((round(width*scale), round(height*scale)))

    if negative == True:
        img = ImageOps.invert(img)
        
    if dithering == True:
        img = img.convert("1").convert("L")
        threshold = 1
    
    pixels = img.load()
    width, height = img.size
    for x in range(0, width):
        for y in range(0, height):
            pixels[x, y] = min(1, pixels[x, y]//threshold)

    newsize_x = width//2*2
    newsize_y = height//4*4

    new = Image.new(mode="L", size=(newsize_x, newsize_y))
    new.paste(img, (0, 0))
    pixels = new.load()

    result = ""
    for y in range(0, newsize_y, 4):
        for x in range(0, newsize_x, 2):
            pattern = []
            for offset in range(0, 4):
                row = [pixels[x, y+offset],
                       pixels[x+1, y+offset]]
                pattern.append(row)
            result += encode_pattern(pattern)
        result += "\n"
    
    return result[:-1]

def encode_pattern(pattern):
    sorted_pattern = [0]*8
    for i in range(0, 3):
        row = pattern[i]
        sorted_pattern[i] = row[0]
        sorted_pattern[i+3] = row[1]
        
    sorted_pattern[6] = pattern[3][0]
    sorted_pattern[7] = pattern[3][1]
    sorted_pattern = list(map(str, sorted_pattern[::-1]))

    num1 = int("".join(sorted_pattern),2)
    num2 = 10240 + num1
    char = chr(num2)
    return char

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert images to braille unicode characters.")
    parser.add_argument("path", help="The path to the image that you want to convert.")
    parser.add_argument("-d", "--dithering", action="store_true", help="Enable dithering.")
    parser.add_argument("-n", "--negative", action="store_true", help="Invert the image before coverting.")
    parser.add_argument("-s", "--scale", type=float, required=False, default=1, help="Scale the image by this amount. If this is set the program will ignore SIZEX and SIZEY.")
    parser.add_argument("-t", "--threshold", type=float, required=False, default=100, help="Any pixels over this value will be recorded as white, any below will be recorded as black. This option does nothing if dithering is enabled. Values range from 1-255.")
    parser.add_argument("-y", "--sizey", type=float, required=False, default=-1, help="Resize the image to this height before converting it. SIZEX also has to be set for this to do anything.")
    parser.add_argument("-x", "--sizex", type=float, required=False, default=-1, help="Resize the image to this width. Keep in mind that each character is 2x4 pixels.")
    args = parser.parse_args()

    if args.sizey != -1 and args.sizex != -1:
        size = (args.sizex, args.sizey)
    else:
        size = None
    result = convert_image(args.path, dithering=args.dithering, negative=args.negative, scale=args.scale, threshold=args.threshold, size=size)
    print(result)
