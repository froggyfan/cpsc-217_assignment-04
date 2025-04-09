#
#  CPSC 217, Winter 2025, Assignment 04 -- Emma Berg, UCID 30257840
#
#  Decode the text contained within a .okti file, and display the image
#  created by the pixels therein contained.
#
#  This program includes the necessary modifications for the A+ portion of
#  the assignment.
#



# Import the necessary libraries for this program.
import sys
from SimpleGraphics import *


#
##
###### Function definitions:


#
#  Retrieve the name of the .okti file used for input.
#
#  Parameters:
#   None
#
#  Returns:
#   fname: The name of the .okti file, as determined by the following:
#   - If one Command-Line Argument (CLA) was provided on startup: fname is CLA.
#   - If no CLA was provided on startup: fname comes from prompted user input.
#   - If 2+ CLAs were provided: An error is reported, and the program is closed.
#
def getFileName():
  # If user provided one command line argument, use that as the file name
  if len(sys.argv) == 2:
    fname = sys.argv[1]
    return fname

  # If user didn't provide a command line argument, prompt them for file name
  elif len(sys.argv) == 1:
    fname = input("Enter the name of the input file: ")
    return fname

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
#   -If all validation checks were passed:
#     fileStr: The provided input file, converted into a string, with its first
#              two lines and all of its newline characters removed.
#     xdim: The x-dimension, or width, of the image in pixels
#     ydim: The y-dimension, or height, of the image in pixels
#   
#   -If any validation checks were failed:
#     An appropriate error message is reported, and an exception is raised.
#
def validateFile(fname):
  # Check that the file exists.
  try:
    inf = open(fname, "r")
  # If file does not exist, print the (missing) file name out to the user, and
  # raise a FileNotFoundError exception.
  except:
    print("The indicated file, \""+str(fname)+ \
          "\", was not found. Quitting program...")
    raise FileNotFoundError

  
  else:
    # Check that the file is an OKTI file, by ensuring the first line is
    # "okti". If the first line is not "okti", print the line out to the user,
    # and raise a ValueError exception.
    line = inf.readline().rstrip()
    if line != "okti":
      print("Line 1 of the file, \""+line+\
            "\", was not the expected string \"okti\";")
      print("The provided file is not an OKTI file. Quitting program...")
      raise ValueError


    # Check that image dimensions are present, and are greater than zero.
    # If image dimensions are missing or are less than zero, print Line 2 of
    # the file out to the user, and raise a ValueError exception.
    line = inf.readline().rstrip()
    try:
      xdim = int(line.split(" ")[0])
      ydim = int(line.split(" ")[1])
    except:
      print("Line 2 of the file, \""+line+\
            "\", does not contain integer image dimensions.")
      print("Quitting program...")
      raise ValueError
    if xdim <= 0 or ydim <= 0:
      print("The provided dimensions, width="+str(xdim)+", height="+str(ydim)+\
            ", are invalid;")
      print("One or more of the dimensions was not greater than zero."+\
            " Quitting program...")
      raise ValueError


    # Check that only valid pixel types are present. If an invalid pixel type
    # is present, allow validateTypes to print out the line containing the
    # offending pixel, and then raise a ValueError exception.
    if validateTypes(fname) == False:
      print("Quitting program...")
      raise ValueError

    # Convert the text inside the input file into a string, and remove all
    # of the newline characters it contains.
    fileStr = inf.read()
    fileStr = fileStr.replace("\n","").replace("\r","")

    # Close the input file, and return the values taken from it.
    inf.close()
    return fileStr, xdim, ydim




#
#  Iterate through the pixels described by the body of a .okti file, and check
#  that every pixel is of a valid type.
#
#  Parameters:
#   fname: The name of the .okti file to be checked.
#
#  Returns:
#   -If all pixels were of valid types: Returns a boolean value True.
#   -If any pixel was of invalid type:
#       Prints out the line containing the offending pixel,
#       and returns a boolean value False.
#
def validateTypes(fname):
  # Open the indicated .okti file, and get rid of the first two lines.
  inf = open(fname, "r")
  line = inf.readline()
  line = inf.readline()

  # Initialize the variables for the following while loop.
  index = 0
  lineNumber = 3
  
  # Create a dictionary containing the character-lengths that correspond to
  # each pixel type, as represented by their initial letter.
  pixelTypes = {"p":7, "d":4, "R":3, "I":3, "r":2, "i":2}

  # Read the next line from the file.
  line = inf.readline().rstrip()
  # As long as the line is not empty, check the first character of the line,
  # and then advance by as many indices as is dictated by the dictionary.
  while line != "":
    while index < len(line):
      
      if line[index] in pixelTypes:
        index = index + pixelTypes.get(line[index])

      # If the examined character is not in the dictionary of valid pixel types,
      # print out the current line number as well as the current line, before
      # closing the file and returning False.
      else:
        print("An invalid pixel type was encountered in the file, at line "\
              +str(lineNumber)+":")
        print(line)
        file.close()
        return False

    # Read the next line from the file, reset the index to zero, and increase
    # the count of the current line number by one.
    line = inf.readline().rstrip()
    index = 0
    lineNumber = lineNumber + 1

  # As no invalid pixels were encountered; close the file and return True.
  inf.close()
  return True




#
#  Decode the contents of a .okti file, and arrange each decoded pixel onto
#  the provided picture.
#
#  Parameters:
#   inf: The contents of a .okti file, in string format.
#   picture: The SimpleGraphics image object for the pixels to be placed into.
#   
#  Returns:
#   None -- the picture that was passed as a parameter is modified to
#   contain all of the decoded pixels from the input file.
#
def decodePixels(inf, picture):
  # Initialize the variables and lists used in the upcoming while loop.
  x = 0
  y = 0
  index = 0
  colourList = ["000000"]
  lastColour = [0,0,0]

  # Determine the x-dimension, or width, of the picture.
  xdim = getWidth(picture)

  # As long as the index of the current character-to-be-examined is less than
  # the length of the file, continually execute this loop.
  while index < len(inf):
    
    # If current character is "p", the pixel is of Full RGB Values type;
    if inf[index] == "p":
      # Obtain the red, green, and blue values directly from the following
      # six characters.
      r = int(inf[index+1:index+3], 16)
      g = int(inf[index+3:index+5], 16)
      b = int(inf[index+5:index+7], 16)

      # Check if colour is in the list of previously-encountered colours.
      prevColours(inf[index+1:index+7], colourList)
      # Set the last-used colour to be the current colour.
      lastColour = [r,g,b]
      # Advance index by seven, to line up with the start of the next pixel.
      index = index + 7

      # Increase x-position of pixel by one.
      x = x+1
      # If the end of the row of pixels has been reached, move to the next row,
      # and reset x-position to zero.
      if x == xdim:
        x = 0
        y = y+1

      # Place a pixel on the picture, with the previously-determined values.
      putPixel(picture, x, y, r, g, b)



    # If current character is "d", the pixel is of RGB Differences type;
    elif inf[index] == "d":
      # Obtain the red, green, and blue values by applying the difference
      # in each channel to the RGB values of the last-used colour.
      r = lastColour[0] + ( int(inf[index+1], 16) - 8 )
      g = lastColour[1] + ( int(inf[index+2], 16) - 8 )
      b = lastColour[2] + ( int(inf[index+3], 16) - 8 )

      # Format each colour channel as a hexadecimal number, and check if the
      # total colour is in the list of previously-encountered colours.
      prevColours("{:02x}".format(r) + "{:02x}".format(g) + \
                  "{:02x}".format(b), colourList)
      # Set the last-used colour to be the current colour.
      lastColour = [r,g,b]
      # Advance index by four, to line up with the start of the next pixel.
      index = index + 4

      # Increase x-position of pixel by one.
      x = x+1
      # If the end of the row of pixels has been reached, move to the next row,
      # and reset x-position to zero.
      if x == xdim:
        x = 0
        y = y+1

      # Place a pixel on the picture, with the previously-determined values.
      putPixel(picture, x, y, r, g, b)



    # If current character is "i", the pixel is of Small Indices type;
    elif inf[index] == "i":
      # Obtain the red, green, and blue values from those of the colour at the
      # specified index within the list of previously-encountered colours.
      colour = colourList[int(inf[index+1], 16)]
      r = int(colour[0:2], 16)
      g = int(colour[2:4], 16)
      b = int(colour[4:], 16)

      # Set the last-used colour to be the current colour.
      lastColour = [r,g,b]
      # Advance index by two, to line up with the start of the next pixel.
      index = index + 2
      
      # Increase x-position of pixel by one.
      x = x+1
      # If the end of the row of pixels has been reached, move to the next row,
      # and reset x-position to zero.
      if x == xdim:
        x = 0
        y = y+1

      # Place a pixel on the picture, with the previously-determined values.
      putPixel(picture, x, y, r, g, b)



    # If current character is "I", the pixel is of Large Indices type;
    elif inf[index] == "I":
      # Obtain the red, green, and blue values from those of the colour at the
      # specified index within the list of previously-encountered colours.
      colour = colourList[int(inf[index+1:index+3], 16)]
      r = int(colour[0:2], 16)
      g = int(colour[2:4], 16)
      b = int(colour[4:], 16)

      # Set the last-used colour to be the current colour.
      lastColour = [r,g,b]
      # Advance index by three, to line up with the start of the next pixel.
      index = index + 3
      
      # Increase x-position of pixel by one.
      x = x+1
      # If the end of the row of pixels has been reached, move to the next row,
      # and reset x-position to zero.
      if x == xdim:
        x = 0
        y = y+1

      # Place a pixel on the picture, with the previously-determined values.
      putPixel(picture, x, y, r, g, b)



    # If current character is "r", the pixel is of Short Runs type;
    elif inf[index] == "r":
      # Obtain the red, green, and blue values directly from those of the
      # last-used colour.
      r = lastColour[0]
      g = lastColour[1]
      b = lastColour[2]

      # Obtain the length of the span of identical pixels from the character
      # immediately after the character-type-indicator.
      span = int(inf[index+1], 16)
      # Advance index by two, to line up with the start of the next pixel.
      index = index + 2

      # For as many pixels as were indicated by the span;
      for i in range(span):
        # Increase x-position of pixel by one.
        x = x+1
        # If the end of the row of pixels has been reached, move to the next
        # row, and reset x-position to zero.
        if x == xdim:
          x = 0
          y = y+1

        # Place a pixel on the picture, with the previously-determined values.
        putPixel(picture, x, y, r, g, b)



    # If current character is "R", the pixel is of Long Runs type;
    elif inf[index] == "R":
      # Obtain the red, green, and blue values directly from those of the
      # last-used colour.
      r = lastColour[0]
      g = lastColour[1]
      b = lastColour[2]

      # Obtain the length of the span of identical pixels from the two
      # characters immediately after the character-type-indicator.
      span = int(inf[index+1:index+3], 16)
      # Advance index by three, to line up with the start of the next pixel.
      index = index + 3

      for i in range(span):
        # Increase x-position of pixel by one.
        x = x+1
        # If the end of the row of pixels has been reached, move to the next
        # row, and reset x-position to zero.
        if x == xdim:
          x = 0
          y = y+1

        # Place a pixel on the picture, with the previously-determined values.
        putPixel(picture, x, y, r, g, b)




#
#  Check if a colour is in the list of the 256 previously used colours.
#
#  Parameters:
#   colour: A given colour, in RRGGBB hexadecimal format.
#   colourList: The list of colours to be checked against.
#
#  Returns:
#   None -- the colourList that was passed as a parameter is modified:
#   -If indicated colour was not in list: colour is added to front of the list.
#   -If indicated colour was already in list: list does not change.
#   -If list has more than 256 values: the last item in the list is removed.
#
def prevColours(colour, colourList):
  
  if colour not in colourList:
    colourList.insert(0, colour)
  if len(colourList) > 256:
    colourList.pop()



#
#  Decode the text data from a .okti file, and display the image it represents.
#
#  Parameters:
#   fname: The name of .okti input file.
#
#  Returns:
#   picture: A SimpleGraphics image object containing the pixels described
#            in the .okti file.
#   xdim: The x-dimension, or width, of the picture.
#   ydim: The y-dimension, or height, of the picture.
#
def decodeOKTI(fname):

  # Ensure the input file is valid, and close the program if an exception
  # is raised.
  try:
    fileStr, xdim, ydim = validateFile(fname)
    
  except:
    close()
    quit()

  # If the input file is valid, decode its data and create a SimpleGraphics
  # image object from its contents.
  else:
    picture = createImage(xdim, ydim)
    decodePixels(fileStr, picture)

  return picture, xdim, ydim




def main():
  # Get the name of the .okti file, either from standard input, or from the
  # provided command-line argument, if given.
  fname = getFileName()

  # Create a SimpleGraphics image object, containing the pixels described in
  # the named .okti file.
  picture, xdim, ydim = decodeOKTI(fname)

  # Resize the canvas to fit the image, and draw the image in the top-left
  # corner of the canvas.
  resize(xdim, ydim)
  drawImage(picture, 0, 0)



####### End of function definitions.
##
#



# Call the main function.
main()

