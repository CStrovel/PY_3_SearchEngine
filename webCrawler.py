# Imports 
from os import system, name
from urllib.request import urlopen
import re

# regular expression obects 
link_re = re.compile(r"<a\s+href\s*=\s*(.+?)\s*>", re.M|re.S)
def main():

    # Menu driver, get user selection
    # and then execute appropriate function 
    selection = menu(testList)
    if(selection == 1):
        pgs, lnks = crawler("https://docs.python.org/3/library/re.html", 0, 0)
        print(lnks)

def menu(lst):
    "Creates a menu, gets input, and perform validation"
    # variables
    buffer = 0 
    choice = 0 

    # validate number range 
    while choice <= 0 or choice > len(lst):
        # Show table and get user input 
        drawTable(lst)
        buffer = input("Please make a selection: ")
        # validate and convert
        try:
            choice = int(buffer)
        
        except ValueError:
            print("Invalid Input")
             
    return choice 

def drawTable(lst, pad = 0, clr = True):
    "Draws a table around a list of items"
    # Declare ascii character constants
    HOR = '\u2550'
    TLC = '\u2554'
    TRC = '\u2557'
    SID = '\u2551'
    LLC = '\u255A'
    LRC = '\u255D'
    
    # Declare Msc Variables
    counter = 1 
    width = 0 

    # Measure longest element in list
    for s in lst:
        if len(s) > width:
            width = len(s)

    # Adjust for characters, numbering and padding
    width += 5 + (len(lst) // 10) + pad

    # construct menu table
    if clr: clear() 
    print(TLC + (HOR * width) + TRC)
    for s in lst:
        # set field width
        fstr = "{0:" + str(width) + "}"
        # display option  
        print(SID + fstr.format(str(counter) + ") " + s) + SID)
        counter += 1 
    print(LLC + (HOR * width) + LRC)
    
    return 0 

def clear():
    "Determines system and clears the screen appropriatly"

    # Code retrieved form geeksforgeeks.org
    # https://www.geeksforgeeks.org/clear-screen-python/
    if name == 'nt':
        _ = system('cls')

    else:
        _ = system('clear')

    return 

def crawler(tgt, iterate, current, oldLst = []):
    """ Crawls target URL, follows links upto iteration limit,

    returns all found pages in a string list"""
    pages = []
    linkLst = []
    newLst = []

    # retrieve page 
    pages.append(getPgSrc(tgt))

    # Check for any navicable links if below iteration limit
    # ensure only unique links
    linkLst = set(link_re.findall(pages[0])[1] + oldLst)

    # can't change link list durring iteration, so new list must
    # be created 
    paramLLst = linkLst

    # iterate through link list and check sublinks 
    for lnk in linkLst and current != iterate:
        newPg, newLst = crawler(lnk, iterate, current + 1, paramLLst)
        # append results to existing lists 
        paramLLst = set(paramLLst + newLst)
        pages += newPg

    # return all the pages and a list of links already checked 
    return pages, set(linkLst + paramLLst)

def getPgSrc(tgtURL):
    """Returns HTML of specified URL as a string"""
    # code borrowed from my own paraCount.py program
    # Default encoding "best guess"
    encode = 'utf-8'

    # Extract page HTML object
    with urlopen(tgtURL) as req:
        # read incoding information if available, otherwise
        # default to utf-8 
        if req.info().get_content_charset():
            encode = req.info().get_content_charset()

        # decode the HTML object to string 
        page = req.read().decode(encode)

    return page





# test pad
testList = ["Crawler", "Parser", "Indexer", "Scoring","Surf"]

main()
input()