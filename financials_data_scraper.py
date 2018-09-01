#!/usr/bin/env python3

import urllib.request, os.path, csv, sys
from modules import nasdaq_symbols, log_error, scrape_write_data
from bs4 import BeautifulSoup

# Option 1
# Manually set the stock symbols for the companies, eg stock_symbols = ("AMZN", "NFLX", "TSLA")
# stock_symbols = () 

# Option 2
# nasdaq_symbols.get_nasdaq() returns a list of every publicly traded company currently listed on the Nasdaq
# Use w/ care!
# stock_symbols = nasdaq_symbols.get_nasdaq() 

financial_statements = ("financials", "balance-sheet", "cash-flow")

# Scrape annual financial report data from Yahoo Finance (YF) and write to local CSV files
def main(stock_symbols):
    # Create main dir
    main_dir = "Financial Data"
    if os.path.isdir(main_dir) == False:
        os.mkdir(main_dir)

    # Create symbol dir and set company
    for symbol in stock_symbols:
        sym_dir = f"{main_dir}/{symbol}"
        if os.path.isdir(sym_dir) == False:
            os.mkdir(sym_dir)

        # Set company statement and send request to YF
        for statement in financial_statements:
            # If file already exists and has content, move on to next statement
            # This ensures that you can stop and restart script w/out rewriting content already written to file
            filepath = f"{sym_dir}/{symbol}_{statement}.csv"
            if os.path.exists(filepath):
                with open(filepath, "r") as file:
                    if file.readlines() != []: # satisified if content is already written to file
                        file.close()
                        continue
                    else:
                        file.close()
               
            try:
                url = f"https://finance.yahoo.com/quote/{symbol}/{statement}?p={symbol}"
                statement_url = urllib.request.urlopen(url, timeout=2)
            except:
                # Log error, remove already created dir for company, and move on to next company
                log_error.write_error(f"{sys.exc_info()[1]}.\nRecheck the URL: {url}.")
                try:
                    os.rmdir(sym_dir)
                # If dir is not empty, log error
                except:
                    log_error.write_error(f"{sys.exc_info()[1]}\n{symbol} directory could not be removed because it has content.")
                break

            # Open new CSV file, scrape/write data, close file
            if statement_url.status == 200:
                # If request results in redirected url, remove created dir for company and move on to next company
                if statement_url.url == f"https://finance.yahoo.com/lookup?s={symbol.upper()}":
                    log_error.write_error(f"There was a redirect to Yahoo Finance's lookup page.\nRecheck the stock symbol: {symbol}.")
                    try:
                        os.rmdir(sym_dir)
                    # If dir is not empty, log error
                    except:
                        log_error.write_error(f"{sys.exc_info()[1]}\n{symbol} directory could not be removed because it has content.")
                    break

                new_csv = open(filepath, "w") 
                csv_writer = csv.writer(new_csv, quoting=csv.QUOTE_MINIMAL)
                    
                soup = BeautifulSoup(statement_url, "html.parser")
                scrape_write_data.scrape_write(soup, csv_writer)
                new_csv.close() 
            else:
                log_error.write_error(f"The returned HTTP code is: {url.status}.")

if __name__ == "__main__": main(stock_symbols)