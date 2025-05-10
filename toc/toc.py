#!/usr/bin/env python

"""
(copied from https://github.com/msb/toc)

Produces a table of contents for the set of PDF files found in <pages_dir> (each assumed to be a
chapter). The title and number of pages of each PDF is inferred from the file name as follows:

    - {TOC entry}.pdf
    - {TOC entry}.pdf
    -  :
    - {TOC entry}.pdf

The number of title pages is read and then
the TOC pages will be written to <pages_dir> and be named:

    - nn.toc.html
    - nn.toc.html
    -   :

where the numbering continues from the title page numbering.
Also a `pdftk cat` command is written to a script that compiles the book
so as to preserve the TOC ordering.

Note that:
    - the order is alphabetic (case insensitive)

Usage:
  toc.py <pages_dir> [--toc-rows=<rows>] [--toc-cols=<cols>]
  toc.py -h | --help

Options:
  -h --help          Show this screen.
  --toc-rows=<rows>  The max number of TOC rows [default: 50].
  --toc-cols=<cols>  The max number of TOC cols [default: 3].
  <pages_dir>        The folder containing the book pages.
"""

import os
import os.path as path
import math
from typing import List, TextIO, Tuple
from docopt import docopt
from pypdf import PdfReader

# A CSS style sheet for the TOC.
STYLE = """
  td {
    font-size: 10px;
  }
  table tr td:nth-child(2), td:nth-child(4), td:nth-child(6), td:nth-child(8), td:nth-child(10) {
    padding-right: 8px;
  }
"""


def main(args):

    # define the parameters
    pages_dir = args['<pages_dir>']
    toc_rows = int(args['--toc-rows'])
    toc_cols = int(args['--toc-cols'])

    num_title_pages, entries, sorted_files = get_entries(pages_dir)

    # Calculate the entries per page and the number of TOC pages.
    entries_per_page = toc_rows * toc_cols
    toc_pages = math.ceil(len(entries) / entries_per_page)

    counted_entries: List[Tuple[str, int]] = []
    # initialise the `page_no` counter
    page_no = toc_pages + num_title_pages + 1

    # create a list of counted entries: each being title and page no.
    for title, length in entries:
        counted_entries.append((title, page_no))
        page_no += length

    write_pdftk_cmd(pages_dir, num_title_pages, sorted_files, toc_pages)

    # for each TOC page ..
    for page in range(toc_pages):
        # .. write an HTML table to a file and ..
        toc_html_name = path.join(pages_dir, f'{(page + num_title_pages):02d}.toc.html')
        with open(toc_html_name, 'w') as toc_html_fd:
            write_toc_html(
                toc_html_fd, toc_rows, toc_cols, entries_per_page, page, counted_entries
            )

def write_pdftk_cmd(
    # the folder containing the book pages
    pages_dir: str,
    # the number of the title pages
    num_title_pages: int,
    # a sorted `List` of song file names
    sorted_files: List[str],
    # the number of TOC pages
    toc_pages: int
):
    """
    Writes a `pdftk cat` command to a script that compiles the book
    """
    with open(path.join(pages_dir, 'compile.sh'), 'w') as compile_sh_fd:
        # build a list of the title and TOC page PDFs
        first_files: List[str] = []
        for i in range(0, num_title_pages):
            first_files.append(f'{i:02}.title-page.html.pdf')
        for i in range(0, toc_pages):
            first_files.append(f'{(num_title_pages + i):02}.toc.html.pdf')
        joined_files = '" "'.join(first_files + sorted_files)
        compile_sh_fd.write(f'pdftk "{joined_files}" cat output ../compiled.pdf')


def write_toc_html(
    # text file object
    toc_html_fd: TextIO,
    # the max numbers of TOC rows in a page
    toc_rows: int,
    # the max numbers of TOC cols in a page
    toc_cols: int,
    # the max number of entries per page (toc_rows * toc_cols)
    entries_per_page: int,
    # the index of the page being written to
    page: int,
    # a list of counted entries: each being title and page no.
    counted_entries: List[Tuple[str, int]]
):
    """
    This function writes a list of TOC entries as an HTML page to a file object.
    The function has to transpose the entries.
    """
    toc_html_fd.write(f'<html><head><style>{STYLE}</style></head><body><table>')

    for row in range(toc_rows):
        toc_html_fd.write('<tr>')
        for col in range(toc_cols):
            index = row + col * toc_rows + entries_per_page * page
            if index < len(counted_entries):
                title, page_no = counted_entries[index]
                toc_html_fd.write(f'<td>{title}</td><td>{page_no}</td>')
        toc_html_fd.write('</tr>')

    toc_html_fd.write('</table></body></html>')


def get_doc_length(pdf_path: str) -> int:
    """Returns a counts of the PDF's pages"""
    reader = PdfReader(pdf_path)
    return len(reader.pages)


def get_entries(pages_dir: str) -> Tuple[int, List[Tuple[str, int]], List[str]]:
    """
    This function lists all the PDF's in `pages_dir` in alphabetic order
    and returns a `Tuple` of:
    - the number of the title pages
    - a `List` of tuples each of which represents the name of the PDF to be used in the TOC
      and it's number of pages.
    - a sorted `List` of song file names.
    The expected PDF format is {TOC entry}.pdf.
    Files with a `template` extension are assumed to be title pages of length 1.
    """
    num_title_pages = 0
    entries = []
    sorted_files = []

    for file_name in sorted(os.listdir(pages_dir), key=lambda k: k.lower()):
        file_root, file_ext = os.path.splitext(file_name)
        if file_ext == '.pdf':
            sorted_files.append(file_name)
            length = get_doc_length(os.path.join(pages_dir, file_name))
            entries.append((file_root, length))
        elif file_ext == '.template':
            num_title_pages += 1

    return num_title_pages, entries, sorted_files


if __name__ == '__main__':
    main(docopt(__doc__))
