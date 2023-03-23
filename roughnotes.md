# Rough Notes
<hr>

### **Compensation Cases**
1. **_Compensation Box present_**
    - Compensation value is 'Neg' (negotiable)
    - No compensation value given
    - Compensation value given. Typically with text e.g
        - Written as "Up to $...."
        - Written as "$... to $..." (i.e multiple dollar signs)
        - Written as '$...k' indicative of thousands

2. **_No Compensation Box present_**
    - Price is written in title
    - Price is written in body (will not be dealing with this case for now)
    - No price given

<br>
<hr>

### **Compensation Cases Continued**
- Will be taking the minimum amount they can earn if given 
  a range. E.g if 22-28 will take 22
- Neg will just be 0
- If the compensation is not in the box, only then will I check the
  title for a price. Will typically look for the '$' and get the following numbers.
    - if no $ present then just look for numbers by themselves (seems not very common)
- For this first run I won't look in the body text for a price
- Need to make a note if the price is /hr or one lump payment
    - Would be v. difficult to find out how many hours a specific gig is,
      so can maybe let user choose how many hours they think they would/want to
      work on a gig then multiply that by the hourly rate
    - Assumption: if a price is given per day the person is only working for *one* day

<br>
<hr>

### **Navigation**
1. First time going on the website just navigate straight to the craigslist boston gigs url
2. Click 'hide duplicates' button so I don't have to deal with that myself in the code
3. Click on the very first gig
4. After this will navigate using the 'Next' arrow on each gig page until the arrow will no longer change the page

_Alternate approach to Navigation_
- use find_elements to get the links of all the gigs on the page first
- navigate to each gig in the list of gig links
- gather data


<br>
<hr>

### **Being 'Human'**
- Set up a user agent for the browser
  - never done this before so still a bit iffy with it.
- Make the amount of time between requests random (uniformity is too robotic)