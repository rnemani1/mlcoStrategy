import v2Scraper

URL = input("Enter a sportsbook.fanduel.com game URL: ")
    
while '@' not in URL:
    URL = input("Enter a sportsbook.fanduel.com game URL: ")
        
letter = input("A or B: ")

if letter == 'A':
    v2Scraper.runA(URL)
    
if letter == 'B':
    v2Scraper.runB(URL)