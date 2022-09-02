A = '-100'
B = '-100'

C = '-100'
D = '-100'

print(A != B or C != D)


'''
try:
    URL = sys.argv[1]
    scraperCode = sys.argv[2]
    
    if scraperCode == 'A':
        v2Scraper.runA(URL)

        if scraperCode == 'B':
            v2Scraper.runB(URL)

    except IndexError:
        raise Exception("Execute: python3 run.py URL A or: python3 run.py URL B")
'''