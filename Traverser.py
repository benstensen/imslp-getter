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

def find_next_link(link):
    if link == None: 
        return None

    time.sleep(0.75)
    print('Waiting...')

    webpage_response = requests.get(link)
    time.sleep(0.05)
    
    link = webpage_response.url
    soup = BeautifulSoup(webpage_response.content, 'lxml')
    if soup.title == None:
        return None
    title = soup.title.contents[0]
    # if re.search('\.pdf', link) != None: 
    #     if not (title in titles): 
    #         print('unfamiliar title')
    #         return link

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

def find_pdf_link(starting_link):
    r_link = ''
    print('Attemping to fetch link to file, please wait...')
    next_link = find_next_link(starting_link)
    while next_link != None:
        r_link = next_link
        next_link = find_next_link(r_link)
    print(r_link)
    return r_link

if __name__ == '__main__':
    find_pdf_link(sys.argv[1])