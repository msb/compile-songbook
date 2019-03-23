#!/usr/bin/env python3

"""
Sorts and merges the PDF's referenced in a set of index files into a single PDF. 
A table of contents is also produced. An optional title and an optional supplement can be added.

Usage:
  compile-songbook.py <output_file> <index_files>... [--title=<file>] [--supplement=<index_file>]
  compile-songbook.py -h | --help

Options:
  -h --help       Show this screen.
  --title=<file>  A PDF to use as the title.
  --supplement=<index_file>  A set of pages to be included as a supplement.
  <output_file>   The name of the merged PDF.
  <index_files>   A set of TSV files that reference the PDF sources.
                  A valid row is defines as <title>\t<source_file>[\t<page_range>]
"""

import io
import tempfile
import csv
from PyPDF2 import PdfFileMerger, PdfFileReader
import os.path as path
from docopt import docopt

TOC_LENGTH = 50


def make_toc(sorted_index, title):
    """
    Make's the TOC by building it in HTML and then converting that to a PDF.

    :param sorted_index: the song index list
    :param title: whether or not there is a title
    :return: a file like object containing the TOC
    """
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
        for tr in range(TOC_LENGTH):
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


def make_supplement_title():
    """
    Make's the supplement title by building it in HTML and then converting that to a PDF.

    :return: a file like object containing the supplement title
    """
    title_html_name = path.join(tempfile.gettempdir(), 'supplement.html')
    with open(title_html_name, 'w') as title_html_fd:
        title_html_fd.write('<html>')
        title_html_fd.write('<head><style>h1 {text-align: center;}</style></head>')
        title_html_fd.write('<body><br><br><br><br><h1>Supplement</h1></body>')
        title_html_fd.write('</html>')

        title_pdf_fd = io.BytesIO()

    from weasyprint import HTML
    HTML(title_html_name).write_pdf(title_pdf_fd)

    return title_pdf_fd


def main(args):

    # a merge of all the index files, keyed on title
    index = {}
    
    for index_file in args['<index_files>']:
        with open(index_file) as index_fd:
            reader = csv.reader(index_fd, delimiter='\t')
            for row in reader:
                if len(row) > 1:
                    index[row[0]] = read_row(row)
    
    # sort the index items by title
    sorted_index = sorted(index.items())

    merger = PdfFileMerger(strict=False)

    # append the title, if there is one
    if args['--title']:
        with open(args['--title'], 'rb') as title_fd:
            merger.append(PdfFileReader(title_fd, strict=False))

    # make and append the TOC
    toc_pdf_fd = make_toc(sorted_index, args['--title'])
    merger.append(PdfFileReader(toc_pdf_fd, strict=False))

    # append the song pages
    for _, row in sorted_index:
        append_song(row, merger)

    # append the supplement, if there is one
    supplement_file = args['--supplement']
    if supplement_file:
        merger.append(PdfFileReader(make_supplement_title(), strict=False))
        with open(supplement_file) as supplement_fd:
            reader = csv.reader(supplement_fd, delimiter='\t')
            for row in reader:
                if len(row) > 1:
                    append_song(read_row(row), merger)

    merger.write(args['<output_file>'])


def append_song(row, merger):
    """
    Appends a song to the document

    :param row: a dict of a row in the song index
    :param merger: the PdfFileMerger
    """
    with open(row['path'], 'rb') as song_fd:
        reader = PdfFileReader(song_fd, strict=False)
        if 'pages' in row:
            merger.append(reader, pages=row['pages'])
        else:
            merger.append(reader)


def read_row(row):
    """
    Converts a song index row to a dict

    :param row: a row from the song index
    :return: a dict representation of that row
    """
    row_dict = {'path': row[1]}
    if len(row) > 2:
        row_dict['pages'] = tuple([int(page) for page in row[2].split(',')])
    return row_dict


if __name__ == '__main__':
    main(docopt(__doc__))
