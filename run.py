from curses import wrapper
import scraper

def main(stdscr):
    stdscr.clear()

    scraper.run("https://sportsbook.fanduel.com/basketball/wnba/seattle-storm-@-washington-mystics-31625562", stdscr)

    stdscr.getch()

def add_new_string(string, stdscr):
    stdscr.clear()

    stdscr.addstr('Hello')

    stdscr.refresh()
    stdscr.getch()

wrapper(main)