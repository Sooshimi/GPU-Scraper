# make sure to install BeautifulSoup first before running
from urllib.request import urlopen # urlopen to grab site pages to scrape
from bs4 import BeautifulSoup as soup # BeautifulSoup to create bs4 url objects
import time
import re

# create column for website
# add in aria, overclockers UK

sites = ['https://www.currys.co.uk/gbuk/search-keywords/xx_xx_30343_xx_xx/3060%2Bti/xx-criteria.html',
         'https://www.currys.co.uk/gbuk/search-keywords/xx_xx_30343_xx_xx/3070/xx-criteria.html',
         'https://www.currys.co.uk/gbuk/search-keywords/xx_xx_30343_xx_xx/3080/xx-criteria.html'
         ]

site_count = len(sites) # counts total URLs in 'sites' list

# function to search and find item details from HTML details passed to it, and handles below error
# AttributeError: 'NoneType' object has no attribute 'html'
def search(items, tag, selector, name):
    # .find() function to find specific item details passed to it
    container = items.find(tag, {selector: name})
    if container is not None: # checks if container is a NoneType
        info = container.text.strip() # gets text and strips extra spaces
    else:
        info = "" # if NoneType, replace with empty string
    return info

# function to search and find url from HTML details passed to it, and handles below error
# AttributeError: 'NoneType' object
def url_search(items, tag, selector):
    # .find() function to find specific item details passed to it
    # uses regex to compile a pattern object
    container = items.find(tag, {selector: re.compile("^http")})
    if container is not None: # checks if container is a NoneType
        link = container.get('href') # gets url
    else:
        link = "" # if NoneType, replace with empty string
    return link

header = False # initialised a False to write csv header once
counter = 0  # counts 'for' loop cycle

for url in sites: # loops for every url in the 'sites' list
    client = urlopen(url) # opens connection and grabs the url
    page = client.read() # reads page
    page_soup = soup(page, "html.parser") # html parser

    # grabs each product
    items = page_soup.findAll("article", "product result-prd stamped clearfix")

    # writes csv file and appends every loop cycle
    with open("GPUs.csv", "a") as file:
        if not header: # 'if' statement runs if header is false. Next 'for' loop cycle will skip this when True
            headers = "Brand,Name,Price,Home Delivery Available,Home Delivery Available,Store Collection,No Stock,URL\n"
            file.write(headers) # writes column headers in first line of the file
            header = True # no longer writes header to file in next 'for' loop cycle

        # searches every item in the 'items' object
        for item in items:
            # calls pre-defined search() function
            # all parameters passed below were manually identified and extracted from the website HTML code
            brand = search(item, "span", "data-product", "brand")
            name = search(item, "span", "data-product", "name")
            price = search(item, "strong", "class", "price")
            home_del_av = search(item, "li", "data-availability", "homeDeliveryAvailable")
            home_del_unav = search(item, "li", "data-availability", "homeDeliveryUnavailable")
            store_col = search(item,"li", "data-availability", "collectInStoreAvailable")
            no_stock = search(item, "li", "class", "nostock")
            page_url = url_search(item, "a", "href")

            # write to csv file
            file.write(brand + "," +
                       name + "," +
                       price + "," +
                       home_del_av + "," +
                       home_del_unav + "," +
                       store_col + "," +
                       no_stock + "," +
                       page_url + "\n")

    counter += 1
    print(f"Site ", str(counter), "of ", str(site_count), "scanned.") # displays progress
    time.sleep(1) # wait (seconds) before loop repeats, to reduce chances of site permission errors

print("Scrape of all sites completed.") # prints to confirm full run