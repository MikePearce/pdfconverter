import os, argparse, sys
import PyPDF2, pdfplumber
from atlassian import Confluence
from pprint import pprint
import mistune
import logging

def main():

    # Grab the args (or not)
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--directory',
                    default=None,
                    dest='directory_path',
                    help='Path to directory of markdown files. Defaults to none. Required',
                    type=str
                    )                    

    parser.add_argument('-u', '--username',
                    default=None,
                    dest='atlassian_user',
                    help='Name of the Atlassian User. Defaults to none. Required',
                    type=str
                    )

    parser.add_argument('-t', '--token',
                    default=None,
                    dest='token',
                    help='Atlassian Token. Defaults to none. Required',
                    type=str
                    )

    parser.add_argument('-l', '--location',
                    default=None,
                    dest='url',
                    help='Atlassian URL. Defaults to none. Should end in /wiki. Required',
                    type=str
                    )    

    parser.add_argument('-p', '--parentid',
                    default=None,
                    dest='parent_id',
                    help='ID of parent page, if you want the new pages to be child pages.. Defaults to None',
                    type=str
                    )        

    parser.add_argument('-s', '--spaceid',
                    default=None,
                    dest='space_id',
                    help='ID of confluence space. Defaults to None. Required',
                    type=str
                    )           


    parser.add_argument('--force',
                    default=False,
                    dest='force_create',
                    help='If set script will not ask for confirmation before creating pages. Defaults to False',
                    action='store_true'
                    )
    parser.add_argument('--delete-pages',
                    default=False,
                    dest='delete_pages',
                    help='If set script will delete any existing pages before creating. Defaults to False',
                    action='store_true'
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
        exit("Hey, you need a token (-t, --token) if you want to actually do anything")   

    # Get all PDF filenames
    if args.force_create is None:
        if input('You are about to create a new page, continue? [N/y]: ').lower() == "y":
           args.force_create = True
    
    if args.force_create is True:
        created_pages = []
        existing_pages = []
        conf = getConfluenceConnection(TOKEN, args.url, args.atlassian_user)
        for file in progressbar(read_MD_title(directory=args.directory_path), "Reading Markdown Files: ", 40):  

            # Does the page exist?
            make_page = True
            if get_confluence_page(conf, args.space_id, file[:-3]) == True:

                # Do we want to delete it?
                if args.delete_pages is True:
                    
                    delete_confluence_page(
                        conf,
                        conf.get_page_id(args.space_id, file[:-3])
                    )
                    
                else:
                    existing_page.append(file[:-3])
                    make_page = False

            if make_page == True:                   
                # Open the file for reading, and write it to an .md file
                created_pages.append(
                    make_confluence_page(
                        conf,
                        space_id=args.space_id,
                        page_name=file[:-3],
                        page_parent=args.parent_id,
                        page_body=mistune.html(read_MD(os.path.join(args.directory_path, file)))
                    )   
                )
                
    else:
        exit("Exiting. You selected not to make a page")

    if len(created_pages) > 0:
        print("You created", len(created_pages), "pages!")
        for page in created_pages:
            print(page)

    if len(existing_pages) > 0:
        print("\n\nThese pages already exist, if you want to make new ones, please delete these")
        for page in existing_pages:
            print(page)

def delete_confluence_page(conf, page_id):
    conf.remove_page(page_id, status=None, recursive=False)

def get_confluence_page(conf, space, page_name):
    return conf.page_exists(space, page_name)

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

def make_confluence_page(confluence, space_id, page_name, page_parent, page_body):
    """
    Write text to a new conflence page.
    space: The space ID (should look like "~123456")
    title: Page title
    body: Page Body
    parent_id: ID of parent page (Can get it from URL)
    """
    #try:
    status = confluence.create_page(
                space=space_id, 
                title=page_name, 
                body=page_body, 
                parent_id=page_parent, 
                editor="v2"
    )

    #except:
    #    exit("Problem creating page.")

    return page_name


def read_MD(filePath, skip_pages=0):

    """Read and return content of a PDF"""
    if filePath is None:
        exit("Error: Please specify a filepath to the markdown file.")

    markdown = ""
    try:
        # create a pdf file object
        with open(filePath) as f:
            markdown = f.read()
        f.close()
    except:
        exit('Error: ['+ filePath + '] cannot be opened. Is the path correct?')
  
    return markdown

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