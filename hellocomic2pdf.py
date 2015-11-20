#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Download comics from hellocomic.com and convert them to PDF's

@author @Lordn__n <lord.the.gatekeeper@gmail.com>
"""

import re
import os
import sys
import glob
import signal
import urllib2

from optparse import OptionParser
from pyquery import PyQuery as pq
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image, PageBreak

args = {}
options = {}
last_page = False
next_page = None
total_images = 0
last_page_get = ''
last_url_get = ''
finish_download = False
downloads_folder = ''
expected_num_of_images = 0
last_comic_name_calculated = None


def get_url(url):
    global last_url_get
    global last_page_get

    if url == last_url_get and len(last_page_get) > 0:
        log('URL "' + url + '" from cache!', 'pagger')
        return last_page_get

    log('Getting URL: "' + url + '"', 'pagger')

    last_url_get = url
    headers = {
        'User-Agent': '@Lordn_n hellocomic2pdf',
        'Accept': '*/*'
    }
    request = urllib2.Request(url, headers=headers)

    try:
        page = urllib2.urlopen(request)
        last_page_get = page.read()
    except urllib2.HTTPError:
        return False

    return last_page_get


def get_image(image, chapter, comic_name, image_name):
    global total_images
    global expected_num_of_images

    directory = downloads_folder + comic_name
    image_file = directory + '/' + image_name + '.jpg'
    percentage = (total_images * 100) / expected_num_of_images

    log('Saving image "' + image_file + '"', 'imager')

    print str(percentage) + '% - ' + image_file

    if not os.path.isfile(image_file):
        f = open(image_file, 'w+')
        f.write(get_url(image))
        f.close()
    else:
        log('Image already exists', 'imager')

    total_images = total_images + 1


def get_images(page):
    page_html = pq(get_url(page))
    pages_pyq = page_html('#e1 option')
    base_url = page[:-(len(page) - page.rfind('/') - 2)]
    comic_name = calculate_comic_name(page)
    directory = downloads_folder + comic_name
    progress_file = directory + '/progress'

    check_progress_file(directory, progress_file)

    for p in range(1, len(pages_pyq) + 1):
        page_url = base_url + str(p)

        if not finish_download:
            image_name = calculate_image_name(page_url)
            image_file = directory + '/' + image_name + '.jpg'

            if not os.path.isfile(image_file) and not in_file(progress_file, image_file):
                current_page_html = pq(get_url(page_url))
                current_image = current_page_html('.coverIssue img').attr.src

                get_image(
                    current_image,
                    calculate_chapter_name(page_url),
                    comic_name,
                    image_name
                )

                f = open(progress_file, 'w+')
                f.write(image_file)
                f.close
            else:
                log('Image ' + image_file + ' already downloaded', 'imager')
        else:
            print 'Bye! You can re-run the script anytime you want and continue the progress.'
            sys.exit(0)


def calculate_comic_name(page):
    global last_comic_name_calculated

    if last_comic_name_calculated is None or last_comic_name_calculated not in page:
        regex = re.search('.com\/(.+)\/c', page)

        if len(regex.groups()) is 1:
            last_comic_name_calculated = regex.group(1)
            return regex.group(1)
        else:
            return page
    elif last_comic_name_calculated is not None:
        return last_comic_name_calculated


def calculate_image_name(page):
    regex = re.search('\/c(.+)\/p(.+)', page)

    if len(regex.groups()) is 2:
        return 'chapter-' + regex.group(1) + '_' + 'page-' + regex.group(2)
    else:
        return page


def calculate_chapter_name(page, type='full'):
    regex = re.search('\/c(.+)\/p(.+)', page)

    if len(regex.groups()) is 2:
        return ('chapter-' if type == 'full' else '') + regex.group(1)
    else:
        return page


def sorted_nicely(l):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


def create_comic(fname, path):
    filename = os.path.join(path, fname + ".pdf")

    if os.path.isfile(filename):
        os.unlink(filename)

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    Story = []
    width = 7.5 * inch
    height = 9.5 * inch

    pictures = sorted_nicely(glob.glob(path + '/chapter*_page*.jpg'))

    for pic in pictures:
        Story.append(Image(pic, width, height))
        Story.append(PageBreak())

    doc.build(Story)
    print '%s created.\nEnjoy! :D' % filename


def init(init_url):
    global options
    global total_images
    global expected_num_of_images

    page = pq(get_url(init_url))
    chapters_pyq = page('#e4 option')
    pages_pyq = page('#e1 option')
    expected_num_of_images = (len(chapters_pyq) * len(pages_pyq))

    print 'There are %i chapters.\nThe first chapter has %i pages.\nAssuming all chapters has the same number of pages; it will be a total %i of images.\n' % (len(chapters_pyq), len(pages_pyq), expected_num_of_images)

    for chapter in chapters_pyq:
        chapter = pq(chapter).attr.value
        get_images(chapter)

    print '\nI download a total of %i images.' % total_images

    path = downloads_folder + calculate_comic_name(chapters_pyq.eq(0).attr.value)
    create_comic(calculate_comic_name(chapters_pyq.eq(0).attr.value), path)

    if options.delete:
        images = sorted_nicely(glob.glob(path + '/chapter*_page*.jpg'))

        for image in images:
            os.unlink(image)

        print 'Images deleted.'

    sys.exit(0)


def valdidate_init_url(url):
    if 'www.hellocomic.com' in url and '/c' in url and '/p' in url:
        return True

    print 'Not a valid URL. It has to be the first page of the first chapter/issue of a comic from www.hellocomic.com/ (For now...)'

    sys.exit(0)


def signal_handler(signal, frame):
    global finish_download

    if signal is 2:  # Ctrl + C
        finish_download = True
        print '\n\nWaiting to complete the current download...'
    else:
        sys.exit(0)


def check_progress_file(directory, progress_file):
    if not os.path.exists(directory):
        os.makedirs(directory)

    if not os.path.isfile(progress_file):
        f = open(progress_file, 'w+')
        f.close()


def in_file(file, search):
    with open(file, 'r') as inF:
        for line in inF:
            if search in line:
                return True
    return False


def log(text, type=None):
    global options

    if options.debug:
        print ('' if type is None else '  [' + type + '] >>> ') + text

signal.signal(signal.SIGINT, signal_handler)

parser = OptionParser()
parser.add_option(
    '-d', '--debug',
    action='store_true', dest='debug', default=False,
    help='Show debug messages.'
)
parser.add_option(
    '-D', '--delete',
    action='store_true', dest='delete', default=False,
    help='Delete all images downloader after the PDF creation.'
)
parser.add_option(
    '-p', '--path',
    action='store', dest='path', default='downloads',
    help='Choose the base path to save the comics.'
)

(options, args) = parser.parse_args()

# Fix the path or send the user to fuck him self
if '.' in options.path or '/' in options.path:
    print 'The path (-p --path) doesn\'t need/support slashes or dots'
    sys.exit(0)
else:
    downloads_folder = './' + options.path + '/'

if len(args) is not 1:
    print 'You need to give a URL from www.hellocomic.com'
    sys.exit(0)

valdidate_init_url(args[0])

init(args[0])
