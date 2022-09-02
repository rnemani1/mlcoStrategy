from curses import wrapper
import v2Scraper
import sys

def main(stdscr):
    stdscr.clear()

    try:
        URL = sys.argv[1]
        scraperCode = sys.argv[2]

        if scraperCode == 'A':
            v2Scraper.runA(URL)

        if scraperCode == 'B':
            v2Scraper.runB(URL)

    except IndexError:
        raise Exception("Execute: python3 run.py URL A or: python3 run.py URL B")

wrapper(main)

#python3 run.py URL A or: python3 run.py URL B
