import Googler
import IMSLPer
import Traverser
import sys

# Driver for IMSLP Getter
def imslp_driver():
    search_term = input("Enter search term: ")
    imslp_link = Googler.get_imslp_link_from_search_term(search_term)
    file_access_link = IMSLPer.get_imslp_file_link(imslp_link)
    pdf_link = Traverser.find_pdf_link(file_access_link)
    return pdf_link

# Invoke from command line. Currently relies on keyboard input during execution
# to fetch final PDF link. 
if __name__ == '__main__':
    if '--help' in sys.argv:
        print('--help: display this message')
        print(f'Usage: python {sys.argv[0]}')
        exit()
    imslp_driver()