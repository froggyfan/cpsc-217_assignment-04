from SimpleGraphics import *

def fullRGB(picture, x, y, pixel):
    r = int(pixel[1:3], 16)
    g = int(pixel[3:5], 16)
    b = int(pixel[5:], 16)
    putPixel(picture, x, y, r, g, b)
    return r, g, b


def main():
    img_width = 10
    img_height = 10
    picture = createImage(img_width, img_height)
    resize(img_width, img_height)
    
    frgb_string = "pff0000"

    
    for y in range(0, img_height):
        for x in range(0, img_width):
            fullRGB(picture, x, y, frgb_string)


    drawImage(picture, 0, 0)
    
    #print(fullRGB(picture, x, y, frgb_string))

main()
