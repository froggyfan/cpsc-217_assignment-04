#
#  CPSC 217, Winter 2025, Assignment 04 -- Emma Berg, UCID 30257840
#
#
import sys
from SimpleGraphics import *

import time
start_time = time.time()

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
    quit()


#
#  Process the input file, and ensure that it meets the conditions required
#  of a properly-formatted OKTI file.
#
#  Parameters:
#   fname: The name of the provided input file. 
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
def validateFile(fname):
  # Check that the file exists
  try:
    file = open(fname, "r")
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
    
    #print("checking if validateTypes == False:")
    if validateTypes(fname) == False:
      #print("Invalid pixel type was detected in file. Quitting program...")
      raise ValueError

    # Close the input file, and return the values taken from it

    # Remove all newline characters from input file
    fileStr = fileStr.replace("\n","").replace("\r","")
    
    file.close()
    return fileStr, xdim, ydim
    



def validateTypes(fname):
  file = open(fname, "r")
  line = file.readline()
  line = file.readline()

  index = 0
  lineNumber = 3
  #pixelTypes = {"p":7, "d":4, "R":3, "I":3, "r":2, "i":2}

  line = file.readline().rstrip()

  while line != "":
    while index < len(line):
      if line[index] == "p":
        index = index + 7
      
      elif line[index] == "d":
        index = index + 4
      
      elif line[index] == "R" or line[index] == "I":
        index = index + 3
      
      elif line[index] == "r" or line[index] == "i":
        index = index + 2
      
      else:
        print("An invalid pixel type was encountered in the file, at line "\
              +str(lineNumber)+":")
        print(line)
        file.close()
        return False

    line = file.readline().rstrip()
    index = 0
    lineNumber = lineNumber + 1
    
  file.close()
  return True



def decodePixels(file, picture, xdim, ydim):
  x = 0
  y = 0
  index = 0
  colourList = ["000000"]
  lastColour = [0,0,0]
  
  while index < len(file):

    if file[index] == "p":
      r = int(file[index+1:index+3], 16)
      g = int(file[index+3:index+5], 16)
      b = int(file[index+5:index+7], 16)

      prevColours(file[index+1:index+7], colourList)
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

      prevColours("{:02x}".format(r) + "{:02x}".format(g) + \
                  "{:02x}".format(b), colourList)
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





def prevColours(colour, colourList):
  
  if colour not in colourList:
    colourList.insert(0, colour)
  if len(colourList) > 256:
    colourList.pop()



def main():
  # Determine name of input file
  fname = fileName()
  # Ensure the input file is valid
  try:
    fileStr, xdim, ydim = validateFile(fname)
  except:
    close()
    quit()

  resize(xdim, ydim)
  picture = createImage(xdim, ydim)
  decodePixels(fileStr, picture, xdim, ydim)
  drawImage(picture, 0, 0)


##########################

# Call the main function.
main()
elapsed_time = time.time() - start_time
print("Elapsed time:","{:.3f}".format(elapsed_time),"seconds")
