import Googler
import IMSLPer
import Traverser

def imslp_driver():
    search_term = input("Enter search term: ")
    imslp_link = Googler.get_imslp_link_from_search_term(search_term)
    file_access_link = IMSLPer.get_imslp_file_link(imslp_link)
    pdf_link = Traverser.find_pdf_link(file_access_link)
    return pdf_link

if __name__ == '__main__':
    imslp_driver()