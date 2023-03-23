import string

# PRICE EXTRACTOR
#-----------------------
def price_extractor(txt):
    """ extract a numerical price from the given string

    Args:
        txt (string): text to remove the price from
                      e.g "it cost $52"
    Return:
        price (float): the price
        price_type (int): -1 = no type
                           0 = per hour
                           1 = one-time price
    """
    txt = txt.lower().replace(',', '') # commas can confuse e.g 20,000
    # almost always when they say '24 hours' it is relating to
    # how soon after the work is done will they get paid.
    txt = txt.replace("24 hours", '') 

    # price is negotiable or no compensation value given
    if "neg" == txt or len(txt) == 0:
        price = 0
        price_type = -1

    # compensation value given
    else:
        for idx, letter in enumerate(txt):
            # value starts with $
            if letter == '$':
                new_txt = txt[idx + 1: ].replace('$', '')
                if new_txt[0] == '-' or new_txt[0] == '+': # odd cases where they put + or - after $
                    new_txt = new_txt[1:]
                break
            else:
                new_txt = txt
            
        # get the actual numbers
        price_nums = []
        for l in new_txt:
            if l not in list(string.ascii_letters) and l != " " and l not in list('-+><~!@#$%^&*:;/'):
                price_nums.append(l)
            else:
                break
        
        
        # if no numbers come after $
        if len(price_nums) == 0:
            price = 0
        else:
            try: # in case e.g emojis slip through
                price = abs(float(''.join(price_nums)))
            except:
                price = 0

            # k = 1000
            for x in list("0123456789 "):
                if f"{x}k" in new_txt:
                    price = price * 1000

        # determine the type of the offered price
        if ("hr" in txt) or ("hour" in txt):
            price_type = 0
        else:
            price_type = 1

    return price, price_type


# TESTING
#------------------------
# you can uncomment this and try them out if you'd like!
"""

# testing price
assert price_extractor("a bc xys $4478 55 is the end of 55 the world")[0] == 4478
assert price_extractor("a bc xys $4478.77 55 is the end of 55 the world")[0] == 4478.77
assert price_extractor("Neg")[0] == 0
assert price_extractor("This is a sentence with no numbers")[0] == 0
assert price_extractor("$8This is a sentence with 2 numbers")[0] == 8
assert price_extractor("$85.")[0] == 85
assert price_extractor("$-85.")[0] == 85
assert price_extractor("a bc xys $4478 k 55 is the end of 55 the world")[0] == 4478000
assert price_extractor("$5k ")[0] == 5000
assert price_extractor("$5-673 ")[0] == 5
assert price_extractor("kabc xyz $5k-673 ")[0] == 5000
assert price_extractor("$50-70k")[0] == 50000
assert price_extractor("$60.12-70k")[0] == 60120
assert price_extractor("$25-$30 per hour. ")[0] == 25
assert price_extractor("$50,000")[0] == 50000
assert price_extractor("$20/hour paid within 24 hours $25/hour if you have a car ")[0] == 20


# testing price type
assert price_extractor("Neg")[1] == -1
assert price_extractor("")[1] == -1
assert price_extractor("$25.00 per hour")[1] == 0
assert price_extractor("$18-20/hr ")[1] == 0
assert price_extractor("$18-20/hr ")[1] == 0
assert price_extractor("$20/hour paid within 24 hours $25/hour if you have a car ")[1] == 0
assert price_extractor("$19.50")[1] == 1
assert price_extractor("1st time Surrogate compensation starts at $50,000 + $1200 screening bonus \
                       (1st $200 within 24 hours of program acceptance)! Experienced surrogates earn more!")[1] == 1
assert price_extractor("Donors who complete the study will be compensated $400 for their time and effort ")[1] == 1

"""