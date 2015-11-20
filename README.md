# hellocomic2pdf
`hellocomic2pdf` is a script to download comics hosted at [hellocomic.com](http://www.hellocomic.com/) to a PDF file.

## Features
- Download any comic from [hellocomic.com](http://www.hellocomic.com/) (If DOM hasn't changed since this last commit.)
- Stop and re-run the script to continue where you left it.
- Show progress (Still under work, but "functional")

Tested under Mac OS X. Should also work on Linux but forget about windows...

## Dependencies
- urllib2
- PyQuery
- reportlab Platypus

## Usage
Place `hellocomic2pdf` somewhere in your `PATH`. And give the URL of any page of the comic you want to download (Ex. `http://www.hellocomic.com/super-cool-comic/c20/p1`).

```
$ hellocomic2pdf http://www.hellocomic.com/super-cool-comic/c20/p1
There are 4 chapters.
The first chapter has 18 pages.
Assuming all chapters has the same number of pages; it will be a total 72 of images.

./downloads/super-cool-comic/chapter-1_page-1.jpg
.
.
.

I download a total of 72 images.
./super-cool-comic/super-cool-comic.pdf created

Enjoy! :D
```

## TODO (Not in order...)
- Add search.
- Be more smart about the given URL (Be able to give any URL related to the comic and find the list of links).
- Add progressbar. (Now it show a progress. But I want to implement [progressbar2](http://pythonhosted.org/progressbar2/))
- Clean this crap.
- Speed the whole thing!

Pull requests are welcome.
