#!/usr/bin/env python3

"""
Compiles a set of PDF index files into a single PDF.

Usage:
  compile-songbook.py <output_file> <index_files>...
  compile-songbook.py -h | --help
  compile-songbook.py --version

Options:
  -h --help  Show this screen.
"""

import io
import tempfile
import csv
from PyPDF2 import PdfFileMerger, PdfFileReader
import os.path as path
from docopt import docopt
from weasyprint import HTML

TOC_LENGTH = 50

def make_toc(sorted_index):
    
    counter = 2
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

    HTML(toc_html_name).write_pdf(toc_pdf_fd)
    
    return toc_pdf_fd


def main(args):
    
    index = {}
    
    for index_file in args['<index_files>']:
        with open(index_file) as index_fd:
            reader = csv.reader(index_fd, delimiter='\t')
            for row in reader:
                if len(row) > 1:
                    index[row[0]] = {'path': row[1]}
                    if len(row) > 2:
                        index[row[0]]['pages'] = tuple([int(page) for page in row[2].split(',')])
    
    sorted_index = sorted(index.items())

    toc_pdf_fd = make_toc(sorted_index)
    
    merger = PdfFileMerger(strict=False)

    reader = PdfFileReader(toc_pdf_fd, strict=False)
    merger.append(reader)
    
    for title, row in sorted_index:
        with open(row['path'], 'rb') as input_fd:
            reader = PdfFileReader(input_fd, strict=False)
            if 'pages' in row:
                merger.append(reader, pages=row['pages'])
            else:
                merger.append(reader)

    merger.write(args['<output_file>'])


if __name__ == '__main__':
    main(docopt(__doc__))

