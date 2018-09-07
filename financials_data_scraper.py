#!/usr/bin/env python3

import urllib.request, os.path, shutil, csv, sys
from modules import nasdaq_symbols, write_logs, scrape_write_data
from bs4 import BeautifulSoup
logger = write_logs.write_log_entry

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
    if os.path.isdir(main_dir):
        logger(f"{main_dir} directory already exists.")
    else:    
        os.mkdir(main_dir)
        logger(f"Created {main_dir} directory.")

    # Create symbol dir and set company
    for symbol in stock_symbols:
        sym_dir = f"{main_dir}/{symbol}"
        if os.path.isdir(sym_dir):
            logger(f"{symbol} directory already exists.")
        else:
            os.mkdir(sym_dir)
            logger(f"Created {symbol} directory.")

        # Set company statement and send request to YF
        for statement in financial_statements:
            # If file already exists and has content, move on to next statement
            # This ensures that you can stop and restart script w/out rewriting content already written to file
            filepath = f"{sym_dir}/{symbol}_{statement}.csv"
            if os.path.exists(filepath):
                with open(filepath, "r") as file:
                    if file.readlines() != []: # satisified if content is already written to file
                        file.close()
                        logger(f"{symbol}'s {statement} data already exists within {symbol} directory.")
                        continue
                    else: 
                        file.close()
                        logger(f"{symbol}'s {statement} file already exists within {symbol} but has no data.")
               
            try:
                url = f"https://finance.yahoo.com/quote/{symbol}/{statement}?p={symbol}"
                statement_url = urllib.request.urlopen(url, timeout=2)
            except:
                # Log error, remove already created dir for company, and move on to next company
                logger(f"{sys.exc_info()[1]}: Recheck the URL: {url}.")
                if len(os.listdir(sym_dir)) > 0:
                    shutil.rmtree(sym_dir)
                    logger(f"{symbol} directory was successfully removed along with its contents.")
                else:
                    os.rmdir(sym_dir)
                    logger(f"The {symbol} directory had no content and was successfully removed.")
                break

            # Open new CSV file, scrape/write data, close file
            if statement_url.status == 200:
                # If request results in redirected url, remove created dir for company and move on to next company
                if statement_url.url == f"https://finance.yahoo.com/lookup?s={symbol.upper()}":
                    # Log error, remove already created dir for company, and move on to next company
                    logger(f"There was a redirect to Yahoo Finance's lookup page. Recheck the stock symbol: {symbol}.")
                    if len(os.listdir(sym_dir)) > 0:
                        shutil.rmtree(sym_dir)
                        logger(f"{symbol} directory was successfully removed along with its contents.")
                    else:
                        os.rmdir(sym_dir)
                        logger(f"The {symbol} directory had no content and was successfully removed.")
                    break

                new_csv = open(filepath, "w") 
                csv_writer = csv.writer(new_csv, quoting=csv.QUOTE_MINIMAL)
                    
                soup = BeautifulSoup(statement_url, "html.parser")
                scrape_write_data.scrape_write(soup, csv_writer)
                new_csv.close()
                logger(f"Wrote {symbol}'s {statement} data to file.")
            else:
                logger(f"The returned HTTP code for {symbol}'s {statement} request is: {url.status}.")

if __name__ == "__main__": main(stock_symbols)