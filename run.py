from curses import wrapper
import scraperA
import scraperB
import sys

def main(stdscr):
    stdscr.clear()

    try:
        URL = sys.argv[1]
        scraperCode = sys.argv[2]

        if scraperCode == 'A':
            scraperA.run(URL, stdscr)

        if scraperCode == 'B':
            scraperB.run(URL, stdscr)

    except IndexError:
        raise Exception("Execute: python3 run.py URL A or: python3 run.py URL B")

wrapper(main)