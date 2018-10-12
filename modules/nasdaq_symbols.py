#!/usr/bin/env python3

# Gets Nasdaq stock symbols, creates a .txt file, and adds symbols to list

import urllib.request

def get_nasdaq():
    # Retrieve, clean, and write Nasdaq data to .txt file
    nasdaq_url = "http://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt"
    nasdaq = urllib.request.urlopen(nasdaq_url)
    if nasdaq.status == 200:
        nasdaq_txt = open("nasdaq.txt", "w")
        for line in nasdaq:
            # eg AAPL|Apple Inc. - Common Stock|Q|N|N|100|N|N
            line = line.decode("utf-8")
            symbol = line.split("|")[0]
            nasdaq_txt.write(symbol + "\n") 
        nasdaq_txt.close()

    # Take stock symbols from created .txt file and add them to list
    stock_symbols = [line.strip() for line in open("nasdaq.txt", "r")]

    # nasdaq.txt and stock_symbols may include non-symbol data which will be caught by error handling
    return stock_symbols