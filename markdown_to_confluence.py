import os, argparse, sys
import PyPDF2, pdfplumber
from atlassian import Confluence
from pprint import pprint
import logging

def main():

    # Grab the args (or not)
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--directory',
                    default=None,
                    dest='directory_path',
                    help='Path to directory of PDFs. Defaults to none.',
                    type=str
                    )                    

    parser.add_argument('-u', '--username',
                    default=None,
                    dest='atlassian_user',
                    help='Name of the Atlassian User. Defaults to none.',
                    type=str
                    )

    parser.add_argument('-t', '--token',
                    default=None,
                    dest='token',
                    help='Atlassian Token. Defaults to none.',
                    type=str
                    )

    parser.add_argument('-l', '--location',
                    default=None,
                    dest='url',
                    help='Atlassian URL. Defaults to none. Should end in /wiki',
                    type=str
                    )    

    parser.add_argument('-o', '--outputdir',
                    default=None,
                    dest='output_dir',
                    help='Directory to write MD files to. Defaults to None',
                    type=str
                    )                             

    # Get dem args
    args = parser.parse_args()   

     # First, TOKEN
    TOKEN = None
    if args.token is not None:
        TOKEN = args.token
    elif os.environ["ATLASSIAN_TOKEN"] is not None:
        TOKEN = os.environ["ATLASSIAN_TOKEN"]
    else:
        print("Hey, you need a token if you want to actuall do anything")   



def read_MD_title(directory):
    """
    Read and return all the file names from the directory
    """
    filenames = []
    files = os.listdir(directory)
    for file in files:
        if os.path.isfile(os.path.join(directory, file)):
            filenames.append(file)

    return filenames

def getConfluenceConnection(TOKEN, url, user):

    try:
        confluence = Confluence(url, user, TOKEN)
    except HTTPError:
        exit(args.atlassianUser, "is not authorised.")

    return confluence    

def make_confluence_page(confluence, page_name, page_parent, title, body):
    """Write text to a new conflence page."""
    # Check they actually want to add a page/
    if input('You are about to create a new page, continue?[N/y]: ').lower() == "y":
        status = confluence.create_page(
                    space="~575838448", 
                    title="This is the new title2xz", 
                    body="This is the body", 
                    parent_id=9768665105, 
                    editor="v2"
        )
    else:
        exit()

    print("Page created!")

def read_MD(filePath, skip_pages=0):

    """Read and return content of a PDF"""
    if filePath is None:
        exit("Error: Please specify a filepath to the markdown file.")

    text = ""

    
    try:
        # create a pdf file object
        markdown = open(filePath, 'rb')
    except:
        exit('Error: ['+ filePath + '] cannot be opened. Is the path correct?')
    
  
    return text

def progressbar(it, prefix="", size=60, file=sys.stdout):
    """
    Simple doodah to print a progress bar thanks to
    https://stackoverflow.com/users/1207193/iambr
    """
    count = len(it)
    if count > 0:
        def show(j):
            x = int(size*j/count)
            file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), j, count))
            file.flush()
        show(0)
        for i, item in enumerate(it):
            yield item
            show(i+1)
        file.write("\n")
        file.flush()    

if __name__ == "__main__":
    main()