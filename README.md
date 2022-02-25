# PDF to Markdown to Confluence
I need to convert some PDFs to confluence pages, so I made a thing. 

## Usage

```
usage: pdf_to_markdown.py [-h] [-d DIRECTORY_PATH] [-o OUTPUT_DIR]

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY_PATH, --directory DIRECTORY_PATH
                        Path to directory of PDFs. Defaults to none.
  -o OUTPUT_DIR, --outputdir OUTPUT_DIR
                        Directory to write MD files to. Defaults to None
```
```
usage: markdown_to_confluence.py [-h] [-d DIRECTORY_PATH] [-u ATLASSIAN_USER] [-t TOKEN] [-l URL] [-p PARENT_ID] [-s SPACE_ID] [--force] [--delete-pages]

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY_PATH, --directory DIRECTORY_PATH
                        Path to directory of markdown files. Defaults to none. Required
  -u ATLASSIAN_USER, --username ATLASSIAN_USER
                        Name of the Atlassian User. Defaults to none. Required
  -t TOKEN, --token TOKEN
                        Atlassian Token. Defaults to none. Required
  -l URL, --location URL
                        Atlassian URL. Defaults to none. Should end in /wiki. Required
  -p PARENT_ID, --parentid PARENT_ID
                        ID of parent page, if you want the new pages to be child pages.. Defaults to None
  -s SPACE_ID, --spaceid SPACE_ID
                        ID of confluence space. Defaults to None. Required
  --force               If set script will not ask for confirmation before creating pages. Defaults to False
  --delete-pages        If set script will delete any existing pages before creating. Defaults to False
```                          