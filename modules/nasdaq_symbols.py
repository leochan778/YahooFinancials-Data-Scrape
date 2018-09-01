#!/usr/bin/env python3

# Retrieve, clean, and write Nasdaq data to txt file

import urllib.request

def get_nasdaq():
    nasdaq_url = "http://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt"
    nasdaq = urllib.request.urlopen(nasdaq_url)
    if nasdaq.getcode() == 200:
        nasdaq_txt = open(f"nasdaq.txt", "w")
        for line in nasdaq:
            # eg AAPL|Apple Inc. - Common Stock|Q|N|N|100|N|N
            line = line.decode("utf-8")
            symbol = ""
            x = 0
            # Assign characters to symbol var one at a time until | is encountered
            while line[x] != "|": 
                symbol += line[x]  
                x += 1 
            nasdaq_txt.write(symbol + "\n") 
        nasdaq_txt.close()

    # Take stock symbols from created nasdaq txt file and add them to list
    nasdaq_txt = open(f"nasdaq.txt", "r")
    lines = nasdaq_txt.readlines()
    stock_symbols = []
    for line in lines: # Strip spaces/carriage returns before appending symbol to list
        stock_symbols.append(line.rstrip("\n "))
    nasdaq_txt.close()

    return stock_symbols

if __name__ == "__main__": main()