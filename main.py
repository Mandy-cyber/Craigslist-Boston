from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random
from pricefunc import price_extractor


def gig_earnings(hrs_per_gig=1):
    """ calculate how much money could be made by doing all the gigs 
        posted on Craigslist Boston

    Args:
        hrs_per_gig (float): how many hours would ideally be spent 
                             working on each gig  if the gig has an
                             hourly rate (default=1)
    Returns:
        final_price (float): how much money could be earned
    """

    # SETTING UP BROWSER
    #-----------------------
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3")
    browser = webdriver.Chrome(options=chrome_options)
    browser.set_window_size(1080, 960)

    # to make the bot seem more 'human'
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36' + \
                '(KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')

    # navigate to page and click the 'Hide Duplicates' filter checkbox
    init_url = "https://boston.craigslist.org/search/sob/ggg#search=1~thumb~0~0" # gigs page
    browser.get(init_url)
    time.sleep(2) # time to load page
    dupButton = browser.find_element(By.NAME, 'bundleDuplicates')
    dupButton.click()
    time.sleep(2) # time for filter to auto apply

    #------------------------------------------------------------------------------
    # GOING THROUGH GIGS
    #---------------------
    gig_prices = {}
    currIdx = -1 # current gig index we are on (really start from 0)
    moreGigs = True # are there more gigs to iter through?

    # first gig on the page (starts off iteration)
    first_gig = browser.find_element(By.CLASS_NAME, 'titlestring')
    first_gig.click()

    while moreGigs:
        currIdx += 1
        time.sleep(0.5) # time to load page
        
        # FIND PRICES
        #-------------
        # find the price of this gig
        try:
            # find compensation box and price if exists
            comp_box = browser.find_element(By.XPATH, 
            """/html/body/section/section/section/div[1]/p""")
            span_ele = comp_box.find_element(By.TAG_NAME, 'span') 

            try:
                text_box = span_ele.find_element(By.TAG_NAME, 'b') # desired subelement not always there
            except:
                text_box = span_ele 
            
            price, price_type = price_extractor(text_box.text) # extract price
            # multiply price if it is of the hourly type
            if price_type == 0:
                price = price * hrs_per_gig
            # print(f"Title: {text_box.text} \n Price: {price}")
            gig_prices[currIdx] = price

        except:
            # if no comp_box then try get price from the gig title
            gig_title = browser.find_element(By.CLASS_NAME, 'postingtitletext')
            gig_title_text = gig_title.find_element(By.ID, 'titletextonly').text
            price, price_type = price_extractor(gig_title_text) # extract price
            # multiply price if it is of the hourly type
            if price_type == 0:
                price = price * hrs_per_gig
            # print(f"Title: {gig_title_text} \n Price: {price}")
            gig_prices[currIdx] = price
        
        # NEXT GIG
        #-------------
        # navigate to the next gig
        try:
            next_arrow = browser.find_element(By.CLASS_NAME, 'next')
            old_url = browser.current_url
            next_arrow.click()
            
            # does the next gig exist
            if browser.current_url != old_url: 
                # clicking shows a new page
                time.sleep(round(random.uniform(0.5,1.5), 2)) # how long to wait before doing next request
            else: 
                # clicking shows the same page
                moreGigs = False
        except:
            # no more gigs to look at
            moreGigs = False


    #---------------------------------------------------------------------------------------
    # FINAL CALCULATIONS & RESULT
    #-----------------------------
    browser.quit() # close the web browser
    final_price = 0
    for key, val in gig_prices.items():
        final_price = final_price + val

    print(f"${round(final_price, 2)}/day doing a total of {len(gig_prices)} gigs--doing each gig for {hrs_per_gig} hours")
    return final_price


#---------------------------------------------------------------------------------------
# RUNNING & USER INPUT
#-----------------------------
hrs = input("How many hours would you be working on each gig (ideally)? ") # can comment this out and leave it to default
final_price = gig_earnings(hrs_per_gig=int(hrs))
