#!/usr/bin/env python3

# Scrapes data from Yahoo Finance page and writes to .csv
# YF puts text w/in <span> tags that are nested in <td> tags (eg <tr><td><span>TEXT</span></td></tr>)
# If there is no text to display w/in a <td>, then there is no <span> (eg <tr><td>-</td></tr>)

def scrape_write(soup, writer):
    table_tag = soup.table
    tablerow_tags = table_tag.findAll("tr")

    # Change "Period Ending" or "Revenue" text in first <tr><td><span> 
    tablerow_tags[0].td.span.string = "Financial Category"
                        
    # For every row, write contents returned from return_row() to .csv
    for tablerow in tablerow_tags:
        tabledata_tags = tablerow.findAll("td")
        span_tags = tablerow.findAll("span")
        
        if len(tabledata_tags) > 1: # Don't write descriptive rows w/ only 1 <td>
            row_contents = []
            
            for tabledata_tag in tabledata_tags:
                # Satisfied if <td> in row has <span> w/ data
                if tabledata_tag.span:  
                    text = tabledata_tag.span.text
                # Satisfied if <td> does not have <span> w/ data and placeholder is needed
                else: 
                    text = None
                row_contents.append(text)
            writer.writerow(row_contents)            