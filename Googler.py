import urllib.parse
import requests
import sys
import re
from bs4 import BeautifulSoup

# Encodes a search term to generate a usable search link.
def get_search_link(search_term):
    search_term = 'site:imslp.org ' + search_term
    return 'https://www.google.com/search?q=' + urllib.parse.quote(search_term, safe='')

# Google has a weird problem where it seems to have double encoded the IMSLP
# links. This should fix it as well as convert characters from % encoding to
# their standard UTF-8 representations, where applicable.
def correct_encoded_URL(bad_url):
    url = re.sub('%252', '%2', bad_url)
    url = url[7 : url.find('&')]
    url = urllib.parse.unquote(url)
    return url
    
# Google Search currently stores result titles as h3 elements.
# Returns an array of h3 elements.
def get_titles(search_link):
    google_response = requests.get(search_link)
    soup = BeautifulSoup(google_response.content, 'lxml')
    return soup.select('h3')

# Remove unwanted categories of results from the result pool.  
def sieve_titles(h3_contents):
    i = 0
    titles = []
    while len(titles) < 11 and i < len(h3_contents):
        if re.search('(^Category:)|(^Talk:)|(^Template:)|(^List of works by)|(^User talk:)', h3_contents[i].string) == None:
            titles.append(h3_contents[i])
        i += 1
    return titles

# Print titles to show the user, aiding in user selection process.
def print_titles(titles):
    i = 1
    for title in titles:
        print(str(i) + '. ' + title.string)
        print('\n')
        i += 1

# Main driver for Googler functionality.
def get_imslp_link_from_search_term(search_term):
    search_link = get_search_link(search_term)
    titles = get_titles(search_link)
    titles = sieve_titles(titles)
    print_titles(titles)
    bad_selection = True
    while bad_selection:
        selection = input(f'Choose a link numbered between 1 and {len(titles)}: ')
        if selection.isdigit() and int(selection) > 0 and int(selection) <= len(titles):
            bad_selection = False
    return correct_encoded_URL(titles[int(selection) - 1].parent['href'])

# Invoke from command line. 
if __name__ == '__main__':
    search_term = sys.argv[1]
    if '--help' in sys.argv:
        print('--help: display this message')
        print(f'Usage: python {sys.argv[0]} "search term"')
        exit()
    print(get_imslp_link_from_search_term(search_term))
    