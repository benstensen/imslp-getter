import requests
import time
import sys
from bs4 import BeautifulSoup

# globals
disclaimer_title = 'Disclaimer - IMSLP: Free Sheet Music PDF Download'
subscribe_title = 'Subscribe - IMSLP: Free Sheet Music PDF Download'
eu_title = 'IMSLP-EU Server Main Page'
ca_title = 'PML-CA Server Main Page'
titles = [disclaimer_title, subscribe_title, eu_title, ca_title]

# Given an IMSLP link as input, returns the next link in the path to the PDF
# link, or None if the program speculates it has reached the PDF already.
def find_next_link(link):
    if link == None: 
        return None

    # You'll see occasional sleeps to respect the servers we're sending GET requests to.
    time.sleep(0.75)
    print('Waiting...')

    # May want to add some code here to handle request timeouts/other errors.
    webpage_response = requests.get(link)
    time.sleep(0.05)
    
    # Make soup. This can take a really long time if the file returned from the server
    # is particularly big (e.g. with a large PDF) so it will be necessary to have some
    # timeout handling for this process.
    link = webpage_response.url
    soup = BeautifulSoup(webpage_response.content, 'lxml')
    
    # If soup doesn't have a title, it's probably not an HTML file. Can handle soup-making
    # issue and this with one check for <!DOCTYPE html>, probably.
    if soup.title == None:
        return None
    title = soup.title.contents[0]

    # If the soup has a title, we check the title against known intermediary page titles to
    # determine how to construct the next link. 
    #
    # If you reach the else at the bottom, PLEASE report the link and title of the page.
    if title == titles[0]:
        # print('landed at disclaimer page...')
        next_extension = soup.select_one('a[href^="/wiki/Special:IMSLPDisclaimerAccept"]').attrs['href']
        return 'https://imslp.org' + next_extension
    elif title == titles[1]:
        # print('landed at subscribe page...')
        tag = soup.select_one('#sm_dl_wait')
        return tag.attrs['data-id']
    elif title == titles[2]:
        # print('landed at eu page...')
        next_extension = soup.select_one('a[href^="/files"]').attrs['href']
        return 'https://imslp.eu' + next_extension
    elif title == titles[3]:
        # print('landed at ca page...')
        next_extension = soup.select_one('a[href^="/files"]').attrs['href']
        return 'https://petruccimusiclibrary.ca' + next_extension
    else: 
        print('landed at unfamiliar page with title ' + title)
        return None

# Main driver for Traverser functionality.
def find_pdf_link(starting_link):
    r_link = ''
    print('Attemping to fetch link to file, please wait...')
    next_link = find_next_link(starting_link)
    while next_link != None:
        r_link = next_link
        next_link = find_next_link(r_link)
    print(r_link)
    return r_link

# Invoke from command line.
if __name__ == '__main__':
    if '--help' in sys.argv or len(sys.argv) == 1:
        print('--help: display this message')
        print(f'Usage: python {sys.argv[0]} "imslp_link"')
        exit()
    find_pdf_link(sys.argv[1])