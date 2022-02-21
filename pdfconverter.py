import os, argparse, sys
import PyPDF2
from atlassian import Confluence
import logging

def main():

    # Grab the args (or not)
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filepath',
                    default=None,
                    dest='pdfFilePath',
                    help='Path to the PDF you want to read. Defaults to none.',
                    type=str
                    )

    parser.add_argument('-u', '--username',
                    default=None,
                    dest='atlassianUser',
                    help='Name of the Atlassian User. Defaults to none.',
                    type=str
                    )

    parser.add_argument('-t', '--token',
                    default=None,
                    dest='token',
                    help='Atlassian Token. Defaults to none.',
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
        print("Hey, you need a github token in an env var if you want the private repos too!")

    logging.basicConfig(level=logging.DEBUG)
    
    try:
        confluence = Confluence("https://mytutor.atlassian.net/wiki", args.atlassianUser, TOKEN)
    except HTTPError:
        print(args.atlassianUser, "is not authorised.")

    if input('You are about to create a new page, continue?[N/y]: ').lower() == "y":
        status = confluence.create_page(
                    space="~575838448", 
                    title="This is the new title2", 
                    body="This is the body", 
                    parent_id=9768665105, 
                    editor="v2"
        )
    else:
        exit()

    print("Page created!")


def read():

    

    if args.pdfFilePath is None:
        exit("Error: Please specify a filepath to the PDF.")

    try:
        # create a pdf file object
        pdfFileObj = open(args.pdfFilePath, 'rb')
    except:
        exit('Error: ['+ args.pdfFilePath + '] cannot be opened. Is the path correct?')
    
    # create a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    for i in range(pdfReader.numPages):
        print("Page", i)
        pageObj = pdfReader.getPage(i)
        #print(pageObj.extractText().replace("\n", ""))
        print(pageObj.extractText())

    # closing the pdf file object
    pdfFileObj.close()

if __name__ == "__main__":
    main()
