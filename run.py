from curses import wrapper
import scraper
import sys

def main(stdscr):
    stdscr.clear()

    try:
        URL = sys.argv[1]
        scraper.run(URL, stdscr)
    except IndexError:
        raise Exception("Execute: python3 run.py URL")

wrapper(main)