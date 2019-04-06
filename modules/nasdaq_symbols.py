#!/usr/bin/env python3
import requests


def request_nasdaq():
    """
    Sends HTTP request for Nasdaq data and writes it to .txt file,
    then calls get_nasdaq() to get stock symbols.
    """
    nasdaq_url = "http://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt"
    nasdaq = requests.get(nasdaq_url, timeout=2)
    if nasdaq.status_code == 200:
        with open("nasdaq.txt", "w") as nasdaq_txt:
            nasdaq_txt.write(nasdaq.content.decode("utf-8"))
        return get_nasdaq()
    else:
        raise Exception(f"HTTP status code is {nasdaq.status_code}")


def get_nasdaq():
    """Gets stock symbols from local nasdaq.txt file."""
    return [line.strip().split("|")[0] for line in open("nasdaq.txt", "r")][1:]