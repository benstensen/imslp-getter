import requests
import sys
import re
from bs4 import BeautifulSoup

def sortSecond(val):
    return val[1]

def has_title_match(title, search_term):
    return search_term.lower() in title.lower()

def get_fileblocks(link):
    imslp_request = requests.get(link)
    soup = BeautifulSoup(imslp_request.content, 'lxml')
    return soup.select('div[class*="we_fileblock_"]:not([class*="we_audio_"])')

def process_fileblocks(fileblocks, search_term):
    fileblock_matches = []
    for entry in fileblocks:
        soup = BeautifulSoup(str(entry), 'lxml')
        elem = soup.select_one('span[title="Download this file"]')
        
        title = ''
        for i in elem.contents:
            if re.search('>', str(i)) == None:
                title += str(i)
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

def print_fileblock_matches(fileblocks, link=False):
    i = 1
    for entry in fileblocks:
        print(f"{i}. Title: {entry[0]}\t {entry[1]} download(s)")
        if link==True: print(f"Link: {entry[2]}")
        i += 1

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
    

if __name__ == '__main__':
    get_imslp_file_link(sys.argv[1])               