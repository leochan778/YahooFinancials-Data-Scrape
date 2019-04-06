import os
import pandas as pd
from collections import OrderedDict



class Statement_String_Error(Exception):
    """Raised when statement parameter is not 'fin', 'cf', or 'bs'."""
    pass



class Financial_Statement:
    """
    Instances of this class are financial statement objects.
    
    Param fin_statement - string. Provided by the Company_Financials class.

    Param _file - Open file object of data created by module financials_data_scraper.
    """
    def __init__(self, fin_statement, _file):
        self._statement_type = fin_statement
        df = pd.read_csv(_file)
        df = df.where(pd.notnull(df), None) # Change NaN to None
        headers = list(df)
        self._categories = list(df[headers[0]]._values)
        self._statement_by_year = OrderedDict()
        for i in range(1, len(headers)):
            year = headers[i]
            year_statement = {}
            for j in range(len(self._categories)):
                try: # Assume most values are floats
                    year_statement[self._categories[j]] = int(df[year][j])
                except:
                    year_statement[self._categories[j]] = df[year][j]
                # amount = int(df[year][j]) if not pd.isna(df[year][j]) else df[year][j]
                # year_statement[self._categories[j]] = amount
            self._statement_by_year[year] = year_statement
            

    def __str__(self):
        return f"{type(self).__name__} object representing {self._statement_type} statements"



class Company_Financials:
    """
    Instances of this class represent a company's financials.
    
    Param directory - string. Directory named after company ticker symbol
    created by module financials_data_scraper.
    """
    def __init__(self, directory):
        statements = os.listdir(f"./Financial Data/{directory}")
        self._company_ticker = directory
        for statement in statements:
            with open(f"./Financial Data/{directory}/{statement}", "r") as f:
                # Create Financial_Statement objects of each statement
                if statement == f"{directory}_financials.csv":
                    self._financials = Financial_Statement("Financials", f)
                elif statement == f"{directory}_cash-flow.csv":
                    self._cash_flow = Financial_Statement("Cash-Flow", f)
                elif statement == f"{directory}_balance-sheet.csv":
                    self._balance_sheet = Financial_Statement("Balance-Sheet", f)           
                    
            
    def __str__(self):
        return f"{type(self).__name__} object representing {self._company_ticker}"


    def get_statement_object(self, statement):
        return self.__select_statement(statement)
         

    def __select_statement(self, statement):
        if statement == "fin":
            return self._financials
        elif statement == "cf":
            return self._cash_flow
        elif statement == "bs":
            return self._balance_sheet
        else:
            raise Statement_String_Error("Parameter statement must be 'fin', 'cf', or 'bs'")
