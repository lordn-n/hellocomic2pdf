# hellocomic2pdf
`hellocomic2pdf` is a script to download comics hosted at [hellocomic.com](http://www.hellocomic.com/) to a PDF file.

Tested under Mac OS X. Should also work on Linux. Forget about windows...

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
- Add progressbar.
- Create a progress-cache file to avoid loading the pages again when re-run.
- Catch SIGINT to prevent un-complete images.
- Clean this crap.
- Speed the whole thing!

Pull requests are welcome.