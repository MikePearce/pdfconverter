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

    # Get the list of ignored words
    try:
        with open("exclusions.txt") as file:
            words_to_find = [line.rstrip() for line in file]          
    except:
        print("Cannot find exclusions.txt, no lines will be excluded.")

    # Get all PDF filenames
    for file in progressbar(read_PDF_title(directory=args.directory_path), "Reading PDF: ", 40):

        # Open the file for reading, and write it to an .md file
        text = read_PDF(os.path.join(args.directory_path, file), skip_pages=0, engine="pdfplumber")
        file_heading = file[:-4]
        file_content="# "+file_heading+"\n\n"+text
        write_to_md(
            filename=os.path.join(args.output_dir, file_heading.strip()+".md"),
            file_content=file_content,
            words_to_find=words_to_find
        )

def write_to_md(filename, file_content, words_to_find=[]):
    """Write fileContent to md file"""
    try:
        # Write the MD file
        with open(filename, "w") as file:
            file.write(file_content)
        # Now strip out nonsense
        with open(filename, "r") as input:
            with open(filename+".tmp", "w") as output:
                # iterate all lines from file
                for line in input:
                    # if substring contain in a line then don't write it
                    if not [word for word in words_to_find if(word in line.strip("\n"))]:
                        output.write(line)

        # replace file with original name
        os.replace(filename+".tmp", filename)            
    except:
        exit("Unable to write to " + filename)

def read_PDF_title(directory):
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

def read_PDF(filePath, skip_pages=0, engine=PyPDF2):

    """Read and return content of a PDF"""
    if filePath is None:
        exit("Error: Please specify a filepath to the PDF.")

    text = ""

    
    try:
        # create a pdf file object
        pdfFileObj = open(filePath, 'rb')
    except:
        exit('Error: ['+ filePath + '] cannot be opened. Is the path correct?')
    
    # create a pdf reader object
    
    if engine == "PyPDF2":    
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        for i in range(pdfReader.numPages):
            if i > skip_pages:
                pageObj = pdfReader.getPage(i)
                text = text+pageObj.extractText()

        # closing the pdf file object
        pdfFileObj.close()
    elif engine == "pdfplumber":
        pdfReader = pdfplumber.open(pdfFileObj)
        for i in range(len(pdfReader.pages)):
            if i > skip_pages:
                pageObj = pdfReader.pages[i]
                text = text+pageObj.extract_text()

        # closing the pdf file object
        pdfFileObj.close()
    else: 
        exit("Unrecognised PDF engine: ", engine)

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