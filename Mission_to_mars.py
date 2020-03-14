#!/usr/bin/env python
# coding: utf-8

# # ## Step 1 - Scraping
# 
# Complete your initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.
# 
# * Create a Jupyter Notebook file called `mission_to_mars.ipynb` and use this to complete all of your scraping and analysis tasks. The following outlines what you need to scrape.
# 

# In[54]:


from bs4 import BeautifulSoup as bs 

import pandas as pd
import requests
import json
import pymongo


# In[2]:


url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
response = requests.get(url)
soup = bs(response.text, 'lxml')


# # NASA Mars News
# 
# * Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
# 
# ```python
# # Example:
# news_title = "NASA's Next Mars Mission to Investigate Interior of Red Planet"
# 
# news_p = "Preparation of NASA's next spacecraft to Mars, InSight, has ramped up this summer, on course for launch next May from Vandenberg Air Force Base in central California -- the first interplanetary launch in history from America's West Coast."
# ```
# 

# In[3]:


p = soup.find_all('p')
for ps in p:
    print(ps.text)


# In[4]:


print(soup.prettify())


# In[5]:


#finding all titles

path = soup.find_all('div',class_="content_title")
path
titles = []
for title in path:
    titles.append(title.text)
    
list_of_titles = [item.strip() for item in titles if str(item)]
list_of_titles


# In[6]:


#finding all paragragh text
path = soup.find_all('div', {"class":"rollover_description_inner"})
path
paragraph = []
for p in path:
    paragraph.append(p.text)
    
list_of_paragraph = [item.strip() for item in paragraph if str(item)]
list_of_paragraph


# # JPL Mars Space Images - Featured Image
# 
# * Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
# 
# * Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.
# 
# * Make sure to find the image url to the full size `.jpg` image.
# 
# * Make sure to save a complete url string for this image.
# 
# ```python
# # Example:
# featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'
# ```
# 

# In[7]:


#navigating path with splinter & chromedriver for windows
from splinter import Browser
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome',**executable_path,headless = False)

url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mar'
browser.visit(url)
html = browser.html
soup_2 = bs(html,'lxml')


# In[8]:


print(soup_2.prettify())


# In[16]:



sources = soup_2.find('article',class_='carousel_item')
mars_image = sources['style']


# In[ ]:


# * Visit the Mars Weather twitter account [here]
# (https://twitter.com/marswxreport?lang=en) and 
# scrape the latest Mars weather tweet from the page. 
# Save the tweet text for the weather report as a variable 
# called `mars_weather`.
# * **Note: Be sure you are not signed in to twitter,
# or scraping may become more difficult.**


# In[17]:


url = "https://twitter.com/marswxreport?lang=en"
response = requests.get(url)
soup_3 = bs(response.text, 'lxml')


# In[18]:


print(soup_3.prettify())


# In[20]:


#finding most recent weather update

weather_update = soup_3.find('p', class_='tweet-text').text

weather_update


# # ### Mars Facts
# 
# # Visit the Mars Facts webpage [here](https://space-facts.com/mars/) 
# # and use Pandas to scrape the table containing facts about the planet 
# #including Diameter, Mass, etc.
# 
# #Use Pandas to convert the data to a HTML table string.
# 

# In[21]:


url = "https://space-facts.com/mars/"
response = requests.get(url)
soup_4 = bs(response.text, 'lxml')


# In[25]:


table = pd.read_html(url)
mars_table = table[0]
mars_earth_table = table[1]


# In[26]:


mars_table


# In[27]:


mars_earth_table


# In[28]:


mars_table.to_html('mars_table.html')
mars_earth_table.to_html('mars_earth_table.html')


# # Mars Hemispheres
# 
# # * Visit the USGS Astrogeology site 
# # (https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
# 
# # * You will need to click each of the links to the 
# # hemispheres in order to find the image url to the full resolution image.
# 
# # * Save both the image url string for the full 
# # resolution hemisphere image, and the Hemisphere title containing 
# # the hemisphere name. Use a Python dictionary to store the data 
# # using the keys `img_url` and `title`.
# 
# # * Append the dictionary with the image url 
# # string and the hemisphere title to a list. This list will 
# # contain one dictionary for each hemisphere.
# 
# 

# In[29]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome',**executable_path,headless = False)

#setting base URL
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)
html = browser.html
soup_4 = bs(html,'html.parser')

#creating empty list for images to be put into
images = []
#creating partial text links
links = ['Cerberus','Schiaparelli','Syrtis','Valles']

#creating look going through each planet in series of links
for each_planet in links:
    
    #clicking the first planet
    browser.click_link_by_partial_text(each_planet)
    #clicking the sample to get the full image, image opens in a new window
    browser.click_link_by_partial_text('Sample')
    #telling splinter to look at the 2nd window
    browser.windows.current = browser.windows[1]
    
    #appending the image to the image list
    images.append(browser.url)
    #going back to the original  url to be set up for the next loop
    browser.visit(url)
    
images


# In[53]:


dictionary_planets = {k: v for k, v in zip(links, images)}
dictionary_planets


# In[55]:


conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# In[58]:


db = client.planets_images_db
collection = db.dictionary_planets
collection

