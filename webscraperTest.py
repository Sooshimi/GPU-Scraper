# make sure to install BeautifulSoup first before running
from urllib.request import Request, urlopen # urlopen to grab site pages to scrape
from bs4 import BeautifulSoup as soup # BeautifulSoup to create bs4 url objects
import time
import re

sites = ['https://www.scan.co.uk/shop/gaming/gpu-nvidia/3175/3176/3177/3221#filter=1&categories=3221%7C3177%7C3176'
         ]

site_count = len(sites) # counts total URLs in 'sites' list

# function to handle below error, and gets text and strips extra spaces
# AttributeError: 'NoneType' object has no attribute 'html'
def handle(find):
    if find is not None: # checks if container is a NoneType
        info = find.text.strip() # gets text and strips extra spaces
    else:
        info = "" # if NoneType, replace with empty string
    return info

# function to handle below error specifically for URLs
# AttributeError: 'NoneType' object
def url_handle(url):
    if url is not None: # checks if container is a NoneType
        link = url.get('href') # gets url
    else:
        link = "" # if NoneType, replace with empty string
    return link

header = False # initialised a False to write csv header once
counter = 0  # counts 'for' loop cycle

for url in sites: # loops for every url in the 'sites' list
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    client = urlopen(req) # opens connection and grabs the url
    page = client.read() # reads page
    page_soup = soup(page, "html.parser") # html parser

    # grabs each product
    items = page_soup.findAll("li", {'class':'product'})

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
            brand = item.find("data-description")
            print(brand)
            # brand = handle(find_brand)
            # name =
            # price =
            # basket =
            # page_url = url_search(item, "a", "href")

            # write to csv file
            # file.write(brand + "\n")

    counter += 1
    print(f"Site ", str(counter), "of ", str(site_count), "scanned.") # displays progress
    time.sleep(1) # wait (seconds) before loop repeats, to reduce chances of site permission errors

print("Scrape of all sites completed.") # prints to confirm full run