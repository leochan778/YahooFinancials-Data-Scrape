# YahooFinance-Data-Scrape
The Python code in this repo scrapes [Yahoo Finance](https://finance.yahoo.com/) for financial report data and writes that data to local .csv files for analysis and visualization. For any specified publicly traded company, it retrieves the annual versions of the three following financial reports from the last four years:

* Income Statement
* Balance Sheet
* Statement of Cash Flows

The functionality of this code depends on the HTML structure and URLs of Yahoo Finance's web pages which may change at any time. 

> This repo is neither affiliated with nor sponsored by Yahoo. Ensure that you read Yahoo's [terms of service](https://policies.oath.com/us/en/oath/terms/otos/index.html).

## Usage
Be nice to Yahoo. ***If you are scraping large amounts of data, you should do so incrementally***. 

Option 1 allows you to manually set which companies you would like to retrieve data from using their stock symbol. 

Option 2 is a massive data harvest that fetches the stock symbols for *all* the companies currently traded on the Nasdaq and in turn uses those symbols to retrieve the financial report data from Yahoo Finance. The Nasdaq symbols are retrieved from a [.txt file](http://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt) that Nasdaq updates regularly. It also creates a local .txt file with the Nasdaq stock symbols.

If you run the script to obtain some data and then stop the script, it can be restarted without having to redo the scraping and file writing that has already been completed. The script will check to see if the particular report already exists; if it does, it will go on to the next.

The most common errors are handled and logged in a .txt file.

## Dependencies
* [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)
* [Requests](http://docs.python-requests.org/en/master/)

## Authors
**Jordan Bradford** - GitHub: [jrdnbradford](https://github.com/jrdnbradford)

## License
This project is licensed under the MIT license. See [LICENSE.txt](LICENSE.txt) for details.