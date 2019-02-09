#!/usr/bin/env python3

"""
Sorts and merges the PDF's referenced in a set of index files into a single PDF. 
A table of contents is also produced. An optional title can be added.

Usage:
  compile-songbook.py <output_file> <index_files>... [--title=<file>]
  compile-songbook.py -h | --help

Options:
  -h --help       Show this screen.
  --title=<file>  A PDF to use as the title.
  <output_file>   The name of the merged PDF.
  <index_files>   A set of TSV files that reference the PDF sources.
                  A valid row is defines as <title>\t<source_file>[\t<page_range>]
"""

import io
import tempfile
import csv
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import os.path as path
from docopt import docopt

TOC_LENGTH = 50

def make_toc(sorted_index, title):
    
    counter = 3 if title else 2
    toc = []
    for title, row in sorted_index:
        toc.append((title, str(counter)))
        if 'pages' in row:
            counter += row['pages'][1] - row['pages'][0]
        else:
            counter += 1

    toc_html_name = path.join(tempfile.gettempdir(), 'toc.html')
    with open(toc_html_name, 'w') as toc_html_fd:
        toc_html_fd.write('<html><head><style>td {font-size: 10px;}</style></head><body><table>')
        for tr in range(TOC_LENGTH - 1):
            toc_html_fd.write('<tr>')
            index = tr
            while index < len(toc):
                toc_html_fd.write('<td>')
                toc_html_fd.write(toc[index][0])
                toc_html_fd.write('</td><td>')
                toc_html_fd.write(toc[index][1])
                toc_html_fd.write('</td>')
                index += TOC_LENGTH
            toc_html_fd.write('</tr>')
        
        toc_html_fd.write('</table></body></html>')

    toc_pdf_fd = io.BytesIO()

    from weasyprint import HTML
    HTML(toc_html_name).write_pdf(toc_pdf_fd)
    
    return toc_pdf_fd


def main(args):

    # a merge of all the index files, keyed on title
    index = {}
    
    for index_file in args['<index_files>']:
        with open(index_file) as index_fd:
            reader = csv.reader(index_fd, delimiter='\t')
            for row in reader:
                if len(row) > 1:
                    index[row[0]] = {'path': row[1]}
                    if len(row) > 2:
                        index[row[0]]['pages'] = tuple([int(page) for page in row[2].split(',')])
    
    # sort the index items by title
    sorted_index = sorted(index.items())

    toc_pdf_fd = make_toc(sorted_index, args['--title'])
    
    merger = PdfFileMerger(strict=False)

    if args['--title']:
        with open(args['--title'], 'rb') as title_fd:
            merger.append(PdfFileReader(title_fd, strict=False))

    merger.append(PdfFileReader(toc_pdf_fd, strict=False))
    
    for title, row in sorted_index:
        with open(row['path'], 'rb') as input_fd:
            reader = PdfFileReader(input_fd, strict=False)
            if 'pages' in row:
                merger.append(reader, pages=row['pages'])
            else:
                merger.append(reader)

    merger.write(args['<output_file>'])


if __name__ == '__main__':
   file1 = PdfFileReader(open('urban_spaceman.pdf', "rb"))
   file2 = PdfFileReader(open('number.pdf', "rb"))
   output = PdfFileWriter()
   page = file1.getPage(0)
   page.mergePage(file2.getPage(0))
   output.addPage(page)

   with open("join.pdf", "wb") as outputStream:
       output.write(outputStream)
#    main(docopt(__doc__))
