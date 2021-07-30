import requests
import sys
import re
from bs4 import BeautifulSoup

# Utility function for sorting processed fileblocks array
def sortSecond(val):
    return val[1]

# Checks title of fileblock against search term
def has_title_match(title, search_term):
    return search_term.lower() in title.lower()

# IMSLP stores download options for scores in <div>s with the class attribute
# 'we_fileblock_n' where n is some number. This selects and returns an array
# of these elements, referred to as fileblocks throughout the program.
def get_fileblocks(link):
    imslp_request = requests.get(link)
    soup = BeautifulSoup(imslp_request.content, 'lxml')
    return soup.select('div[class*="we_fileblock_"]:not([class*="we_audio_"])')

# Based on a search term, selects fileblocks with a match and populates an 
# array with useful information about each fileblock. Returns the array. Each entry 
# is of the form [title, download count, link], sorted by descending download count.
#
# May consider breaking this into smaller functions.
def process_fileblocks(fileblocks, search_term):
    fileblock_matches = []
    for entry in fileblocks:
        soup = BeautifulSoup(str(entry), 'lxml')
        elem = soup.select_one('span[title="Download this file"]')
        
        # title is occasionally split into multiple parts, this joins them into
        # a human readable format.
        title = ''
        for i in elem.contents:
            if re.search('>', str(i)) == None:
                title += str(i)

        # add info to array if the fileblock has a matching title
        # array entry is [title, download count, link]
        if has_title_match(title, search_term):
            fileblock_matches.append([title])
            
            elem = soup.select_one('span[title^="Total number of downloads:"]')
            if elem != None:
                num_dl_str = str(elem['title']).split()
            else: num_dl_str = [0]
            fileblock_matches[-1].append(int(num_dl_str[-1]))

            elem = soup.select_one('span[class="hidden"] a.internal')
            link = elem['href']
            fileblock_matches[-1].append(link)

    fileblock_matches.sort(reverse=True, key=sortSecond)
    return fileblock_matches

# Prints matching fileblock entries for the user. Can set link=True for
# debugging purposes.
def print_fileblock_matches(fileblocks, link=False):
    i = 1
    for entry in fileblocks:
        print(f"{i}. Title: {entry[0]}\t {entry[1]} download(s)")
        if link==True: print(f"Link: {entry[2]}")
        i += 1

# Main driver for IMSLPer functionality. 
def get_imslp_file_link(starting_link):
    fileblocks = get_fileblocks(starting_link)
    fileblock_matches = []
    while len(fileblock_matches) == 0:
        search_term = input("Enter the part to search for, or press enter for unfiltered results: ")
        fileblock_matches = process_fileblocks(fileblocks, search_term)
        if len(fileblock_matches) == 0:
            print("Couldn't find a part with that search term! Try again.")
            continue
        print("Select an option from below:")
        print_fileblock_matches(fileblock_matches)
        bad_selection = True
        while bad_selection == True:
            selection = input(f'Choose a link between 1 and {len(fileblock_matches)}: ')
            if selection.isdigit() and int(selection) > 0 and int(selection) <= len(fileblock_matches):
                bad_selection = False
                link = 'https://www.imslp.org' + str(fileblock_matches[int(selection) - 1][2])
                return link
    
# Invoke from command line.
if __name__ == '__main__':
    if '--help' in sys.argv:
        print('--help: display this message')
        print(f'Usage: python {sys.argv[0]} "imslp_link"')
        exit()
    print(get_imslp_file_link(sys.argv[1]))               