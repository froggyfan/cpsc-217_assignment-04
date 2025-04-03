#
#
#
#
import sys
from SimpleGraphics import *

import time
start_time = time.time()

# Initalize constants:
lastColour = [0,0,0]
colourList = ["000000"]

#
#  Retrieve the name of the .okti file used for input.
#
#  Parameters:
#   None
#
#  Returns:
#   If one Command-Line Argument was provided on startup: returns CLA
#   If no CLA was provided on startup: returns result of prompted user input
#   If 2+ CLA were provided: reports an error, and quits program
#
def fileName():
  # If user provided one command line argument, use that as the file name
  if len(sys.argv) == 2:
    inf = sys.argv[1]
    return inf

  # If user didn't provide a command line argument, prompt them for file name
  elif len(sys.argv) == 1:
    inf = input("Enter the name of the input file: ")
    return inf

  # Else, report there were too many command line arguments, and quit program
  else:
    print("Too many command line arguments were given. Quitting program...")
    close()
    quit


#
#  Process the input file, and ensure that it meets the conditions required
#  of a properly-formatted OKTI file.
#
#  Parameters:
#   file_name: The name of the provided input file. 
#
#  Returns:
#   If all validation checks were passed:
#     file: The provided input file, with the first two lines trimmed off, and
#           all newline characters removed.
#     xdim: The x-dimension, or width, of the image in pixels
#     ydim: The y-dimension, or height, of the image in pixels
#
#   If any validation checks were failed:
#     An appropriate error message is reported, and the program is quit.
#
def validateFile(file_name):
  # Check that the file exists
  try:
    file = open(file_name, "r")
  except:
    print("Indicated file was not found. Quitting program...")
    raise FileNotFoundError
  
  else:
    # Check that the file is an OKTI file
    if file.readline().rstrip() != "okti":
      print("Indicated file was not an OKTI file. Quitting program...")
      raise ValueError

    # Check that image dimensions are present, and are greater than zero
    lineTwo = file.readline().rstrip()
    try:
      xdim = int(lineTwo.split(" ")[0])
      ydim = int(lineTwo.split(" ")[1])
    except:
      print("Dimensions of indicated file were not found. Quitting program...")
      raise ValueError
    if xdim <= 0 or ydim <= 0:
      print("Dimensions of indicated file were invalid. Quitting program...")
      raise ValueError

    # Check that only valid pixel types are present
    fileStr = file.read()
    # Remove all newline characters from input file
    fileStr = fileStr.replace("\n","").replace("\r","")
    
    if validateTypes(fileStr) == False:
      print("Invalid pixel type was detected in file. Quitting program...")
      raise ValueError

    # Close the input file, and return the values taken from it
    file.close()
    return fileStr, xdim, ydim
    



# Editor's note:: could prob remove this / convert it into a general
# pixel-type identifying thing that works per single pixel. Then in the file
# validation function, apply this func to every pixel in the file, and see if
# an error occurs in there. This way u don't have as many 'redundant' funcs.
def validateTypes(inf):
  # Make a copy of input file
  file = inf

  # Check if first character in file is a valid pixel type, then trim the first
  # X-many characters from the file, depending on which type is indicated.
  while len(file) > 0:
    if file[0] == "p":
      file = file[7:]
      
    elif file[0] == "d":
      file = file[4:]
      
    elif file[0] == "R" or file[0] == "I":
      file = file[3:]
      
    elif file[0] == "r" or file[0] == "i":
      file = file[2:]
      
    else:
      return False

  return True



def pixelType(file, picture, xdim, ydim):
  x = 0
  y = 0
  index = 0
  while index < len(file):

    if file[index] == "p":
      r = int(file[index+1:index+3], 16)
      g = int(file[index+3:index+5], 16)
      b = int(file[index+5:index+7], 16)

      prevColours(file[index+1:index+7])
      lastColour = [r,g,b]
      index = index + 7
      
      x = x+1
      if x == xdim:
        x = 0
        y = y+1

      putPixel(picture, x, y, r, g, b)


    elif file[index] == "d":
      r = lastColour[0] + ( int(file[index+1], 16) - 8 )
      g = lastColour[1] + ( int(file[index+2], 16) - 8 )
      b = lastColour[2] + ( int(file[index+3], 16) - 8 )

      prevColours("{:02x}".format(r) + "{:02x}".format(g) + "{:02x}".format(b) )
      lastColour = [r,g,b]
      index = index + 4

      x = x+1
      if x == xdim:
        x = 0
        y = y+1

      putPixel(picture, x, y, r, g, b)


    elif file[index] == "i":
      colour = colourList[int(file[index+1], 16)]
      r = int(colour[0:2], 16)
      g = int(colour[2:4], 16)
      b = int(colour[4:], 16)

      lastColour = [r,g,b]
      index = index + 2
      
      x = x+1
      if x == xdim:
        x = 0
        y = y+1

      putPixel(picture, x, y, r, g, b)


    elif file[index] == "I":
      colour = colourList[int(file[index+1:index+3], 16)]
      r = int(colour[0:2], 16)
      g = int(colour[2:4], 16)
      b = int(colour[4:], 16)

      lastColour = [r,g,b]
      index = index + 3
      
      x = x+1
      if x == xdim:
        x = 0
        y = y+1

      putPixel(picture, x, y, r, g, b)


    elif file[index] == "r":
      r = lastColour[0]
      g = lastColour[1]
      b = lastColour[2]

      span = int(file[index+1], 16)
      index = index + 2

      for i in range(span):
        x = x+1
        if x == xdim:
          x = 0
          y = y+1

        putPixel(picture, x, y, r, g, b)


    elif file[index] == "R":
      r = lastColour[0]
      g = lastColour[1]
      b = lastColour[2]

      span = int(file[index+1:index+3], 16)
      index = index + 3

      for i in range(span):
        x = x+1
        if x == xdim:
          x = 0
          y = y+1

        putPixel(picture, x, y, r, g, b)





def prevColours(colour):
  
  if colour not in colourList:
    colourList.insert(0, colour)
  if len(colourList) > 256:
    colourList.pop()



def main():
  # Determine name of input file
  file_name = fileName()
  # Ensure the input file is valid
  try:
    fileStr, xdim, ydim = validateFile(file_name)
  except:
    close()
  else:
    resize(xdim, ydim)
    picture = createImage(xdim, ydim)
    pixelType(fileStr, picture, xdim, ydim)
    drawImage(picture, 0, 0)

main()
elapsed_time = time.time() - start_time
print("Elapsed time:","{:.3f}".format(elapsed_time),"seconds")
