#!/usr/bin/env python
# coding: utf-8

# In[6]:


from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests


# NASA Mars News
# ---

# In[7]:


#Setup splinter
executable_path = {'executable_path':  '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[8]:


url = 'https://redplanetscience.com/'
browser.visit(url)


# In[9]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[12]:


# Scrape the Mars News Site and collect the latest News Title and Paragraph Text. 
#Assign the text to variables that you can reference later.
news_title = soup.find('div', class_='content_title')
news_p = soup.find('div', class_='article_teaser_body')
    
print(news_title.text)
print(news_p.text)


# In[13]:


browser.quit()


# JPL Mars Space Images - Featured Image
# ---

# In[14]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[15]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')

div = soup.find('div', class_="floating_text_area")

link = div.find('a')
href = link['href']

featured_image_url= f"{url}/{href}"
print(featured_image_url)


# In[16]:


browser.quit()


# Mars Facts
# ---

# In[17]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
url = 'https://galaxyfacts-mars.com/'
browser.visit(url)


# In[19]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[22]:


tables = pd.read_html(url)
tables


# In[23]:


mars_facts_df= tables[0]
mars_facts_df.columns = [['Category', 'Mars Value', 'Earth Value']]
del mars_facts_df['Earth Value']
mars_facts_df


# In[24]:


html_table = mars_facts_df.to_html()
html_table


# In[25]:


html_table_string=html_table.replace('\n', '')


# In[27]:


browser.quit()


# Mars Hemispheres
# ---

# In[28]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
url = 'https://marshemispheres.com/'
browser.visit(url)


# In[29]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[30]:


images = soup.find_all('div', class_='description')

image_list = []
for image in images:
    image_dict = {}
    image_title = image.a.h3.text
    image_dict['title'] = image_title
    
    browser.links.find_by_partial_text(image_title).click()
    
    new_html = browser.html
    new_soup = BeautifulSoup(new_html, 'html.parser')
    
    download = new_soup.find('div', class_='downloads')
    original = download.find_all('li')[1].a['href']
    image_dict['img_url'] = original
    image_list.append(image_dict)
    
    browser.back()

image_list 


# In[31]:


browser.quit()


# In[ ]:




