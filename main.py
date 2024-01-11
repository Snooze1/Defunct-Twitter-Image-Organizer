from cProfile import run
from operator import contains
from bs4 import BeautifulSoup                                 ##Beautiful Soup parses our Twitter link without the need for Twit API
from selenium import webdriver                                 ##Selenium required to bypass "Unsupported browser" access
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


from webdriver_manager.chrome import ChromeDriverManager
from tkinter import Y
from exif import Image
import os
import urllib.request
import requests
import urllib
import re
import msvcrt

#To do:
# Maybe fix web parsing bug?
    #Temp retry solution enabled
      #10-23-22 : Bug is probably just the webpage needing to load fully, discovered by letting it
      #not run in headless and seeing it didn't fully load. Properly looped
# Progress bar maybe?
# User link paste without enter?
# Add emoji support?
# ADD MORE IMAGE FORMATS

#Foreign character img desc support?


########################### FUNCTIONS ###########################

def setpathcharrefs():    ## Hard coded but doesn't matter for me
  charrefs = (r'C:\Users\Snooser\Pictures\Character Refs')
  os.chdir(charrefs)

def setpathdrawrefs():    ## Hard coded but doesn't matter for me
  drawrefs = (r"C:\Users\Snooser\Pictures\DrawRefs")
  os.chdir(drawrefs)

def setpathcategorythree():    ## Hard coded but doesn't matter for me
  categorythree = (r"C:\Users\)
  os.chdir(categorythree)

def setpathnewfolder():
  newfold = os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), 'New Twitter Folder') 
  if not os.path.exists(newfold):                                  ## If a pics folder doesn't exist, make one!
      os.makedirs(newfold)
  #os.chmod(newfold, stat.S_IWRITE)
  os.chdir(newfold)                                                ## Move directory to pics

def recipe(inputsoup):                                             # This function specificies our soup to both only contain image links,
                                                                  # and to only contain them from the "Tweet" portion of the page so it doesn't parse comments
  return inputsoup.find_all(class_="css-1dbjc4n r-18u37iz r-1ny4l3l r-1udh08x r-1qhn6m8 r-i023vh") and inputsoup.find_all(src=re.compile("https://pbs.twimg.com/media/"))

def img_ripper(inputsoup,list):
  findsoups = recipe(inputsoup)                                   ## Gets our findsoups from our recipe                                   
  splitpeasoup = str(findsoups).split("\"")                       ## Splits our findsoup "string" 
  for x in splitpeasoup:                                          ## For every entry in splitpeasoup
      if "https://pbs.twimg.com/media/" in x:                     
        hold = x.split("&")[0]                                    ## Small bit of extra code to chop off the invalid end of link
        
        temp = hold.split("=")[1]
        format = temp.split("&")[0]
        
        
        list.append(hold)                                          ## Appends our cleaned up link to the links list
        list.append(format)

def alphabetsoup(inputsoup):                                            #This function gets the post text
  alpha = str((inputsoup.find(class_="css-1dbjc4n r-1s2bzr4")))         #This creates a soup of just our spans including these css_classes
  #print(alpha)
  alphasplit = re.split("r-qvutc0\">|</span>",alpha)
  i=0
  concatstring = ""
  while i < len(alphasplit):
    if re.match("<div |</div>|<span |</span>|<img ",alphasplit[i]):
      if re.match("role=\"link\">|",alphasplit[i]):
        atparsing = re.split("role=\"link\">|</a>",alphasplit[i])         # Hashtags and @s are stored between the same tags. If detected, the list entries
        if len(atparsing) == 3:                                           # are split further and the important text is concatonated to the
          concatstring+=atparsing[1]                                      # end of our concat string
      i+=1
    else:
      concatstring+=alphasplit[i]
      i+=1
  utf8 = concatstring.encode()                # Encodes to utf8
  return utf8

#################################################################################

#main

userlink = input("Paste your Twitter link: ")                       ## Takes user input on link
#userlink = " "

y=0
while y != 1:                                                       ## Loop that determines where to set the save location
  print(  """
  Press 1 to save into Character Refs
  Press 2 to save into Draw Refs
  Press 3 to save into Category 3
  Press 4 to to create new Twitter Folder on desktop""")
  folderoption = msvcrt.getche()                                    ## Using this instead of input so I don't have to hit enter
  folderopsplit = str(folderoption).split("'")                      ## However we need to split it because it stores it with  extra characters

  if folderopsplit[1] == "1":                                       ## [1] is the position of the actual number in the list
    setpathcharrefs()
    y+=1
  elif folderopsplit[1] == "2":         
    setpathdrawrefs()
    y+=1
  elif folderopsplit[1] == "3": 
    setpathcategorythree()
    y+=1
  elif folderopsplit[1] == "4": 
    setpathnewfolder()
    y+=1
  else:
    y+=1
    print ("Error, invalid entry! Try again!\n")


  
  #op = Options()                             #Loads Chrome as a "blank" process to load webpage but not create window
  #op.add_argument('headless')
  #op.add_argument('--disable-gpu')
  #driver = webdriver.Chrome(chrome_options=op)
  driver = webdriver.Chrome()
  driver.get(userlink)
  print("Loading...")

tries = 0
while tries != 5:
  data = requests.get(userlink).text
  data = driver.page_source

  soup = (BeautifulSoup(data, "html.parser"))                   ## Makes our soup, yumm!
  userrip = ("@" + (userlink.split("/"))[3])                    ## Gets the @ from the user given link
  
  links = []
  
  if soup.find_all(class_="css-1dbjc4n r-1ndi9ce"): ## If we end up having the "sensitive material" button
    print("button :3")
    button = driver.find_element(By.CSS_SELECTOR, 'class="css-18t94o4 css-1dbjc4n r-1niwhzg r-42olwf r-sdzlij r-1phboty r-rs99b7 r-15ysp7h r-4wgw6l r-1ny4l3l r-ymttw5 r-f727ji r-j2kj52 r-o7ynqc r-6416eg r-lrvibr"')
    button.click()
    soup = (BeautifulSoup(data, "html.parser"))
#  
  
  img_ripper(soup,links)
  print(links)
  numofimgs = len(links)
  if numofimgs == 0:
    tries+=1
    print ("Attempt " + str(tries) + " failed, webpage probably hasn't loaded, retrying")
  else:
    tries=5

n = 0
while n != numofimgs:                                                        ## Grabs the amt of images the user specified
  offset = 0  
  newfile = 0
  while newfile != 1:                                                  ## This loop manages everything involved in creating a new file ##
    filename = (userrip+str(n+offset)+"."+format)                               ## Creates a filename
    if os.path.isfile(filename) == True:                                     ## Checks if a file with the assigned filename already exists
      offset+=1                                                              ## If so, increment offset by 1 and check again
    else:
      urllib.request.urlretrieve(links[n],filename)                          ##Saves it to the directory defined earlier from link!
                                                                       ## Next chunk edits exif data ##
      with open(os.getcwd() + "\\" + filename, "rb") as opened_file:         ## Loads file in from current directory as read only (rb)
        currentimg = Image(opened_file)                                      
        ##currentimg.image_description = alphabetsoup(soup)                    ## Saves the result of alphabetsoup to the image_description tag
      with open(os.getcwd() + "\\" + filename, "wb") as opened_file:         ## Changes permission to write allowed
        opened_file.write(currentimg.get_file())                             ## Overwrites the original image with the new exif data

      newfile = 1                                                            ## Exits the loop
  n+=1