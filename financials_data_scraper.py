#!/usr/bin/env python3

import os.path, shutil, csv, sys, requests
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
            # Ensures script can be restarted w/out rewriting data already written to file
            filepath = f"{sym_dir}/{symbol}_{statement}.csv"
            if os.path.exists(filepath):
                with open(filepath, "r") as file:
                    if file.readlines() != []: # Satisified if content is already written to file
                        logger(f"{symbol}'s {statement} data already exists within {symbol} directory.")
                        continue # Move on to next financial statement
                    else:
                        logger(f"{symbol}'s {statement} file already exists within {symbol} but has no data.")
               
            try:
                url = f"https://finance.yahoo.com/quote/{symbol}/{statement}?p={symbol}"
                response = requests.get(url, timeout=2)
                response.raise_for_status()
            except requests.exceptions.RequestException as error:
                logger(f"{error}: Recheck the URL: {url}.")
                remove_dir(sym_dir, symbol)
                break # Move on to next company
            
            # If request results in redirected url
            if response.url == f"https://finance.yahoo.com/lookup?s={symbol.upper()}":
                logger(f"There was a redirect to Yahoo Finance's lookup page. Recheck the stock symbol: {symbol}.")
                remove_dir(sym_dir, symbol)
                break # Move on to next company

            # Open new CSV file, scrape/write data, close file
            new_csv = open(filepath, "w") 
            csv_writer = csv.writer(new_csv, quoting=csv.QUOTE_MINIMAL)
                    
            try:
                soup = BeautifulSoup(response.text, "html.parser")
                scrape_write_data.scrape_write(soup, csv_writer)
            except:
                logger(f"{sys.exc_info()[1]}: Issue with scraping the data for {symbol}'s {statement} file.")
                remove_dir(sym_dir, symbol)
                break # Move on to next company

            new_csv.close()
            logger(f"Wrote {symbol}'s {statement} data to file.")

# Removes dir and logs info
def remove_dir(path, symbol):
    if len(os.listdir(path)) > 0:
        shutil.rmtree(path)
        logger(f"{symbol} directory was successfully removed along with its contents.")
    else:
        os.rmdir(path)
        logger(f"The {symbol} directory had no content and was successfully removed.")

if __name__ == "__main__": main(stock_symbols)