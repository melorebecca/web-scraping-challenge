# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo

def scrape():
     
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    mars_dict ={}
    
    # Mars News URL 
    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    # Retrieve the latest news title and paragraph
    news_title = news_soup.find_all('div', class_='content_title')[0].text
    news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text

    # Mars Image 
    jpl_nasa_url = 'https://spaceimages-mars.com'
    browser.visit(jpl_nasa_url)
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')
  
    div = image_soup.find('div', class_="floating_text_area")
    link = div.find('a')
    href = link['href']
    featured_image_url= f"{jpl_nasa_url}/{href}"

    # Mars facts to be scraped, converted into html table
    facts_url = 'https://galaxyfacts-mars.com/'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    tables = pd.read_html(facts_url)
    
    mars_facts_df= tables[1]
    mars_facts_df.columns = ['Category', 'Mars Value']
    mars_html_table = mars_facts_df
    
    mars_html_table.replace('\n', '')
    mars_html_table = mars_facts_df.to_html(classes= 'table table-striped')
    
    # Mars hemisphere name and images to be scraped
    hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')
    
    # Mars hemispheres 
    images = hemispheres_soup.find_all('div', class_='item')
    hemisphere_title = []
    hemisphere_img_url = []
    
    for x in images:
        #image titles
        hemisphere_title = x.find('h3').text

        url1 = x.find('a', class_= 'itemLink product-item')['href']

        url2 = hemispheres_url + url1
        browser.visit(url2)
        
        #hemisphere images
        html = browser.html
        soup = BeautifulSoup(html,'html.parser')
        
        src = soup.find('img', class_='wide-image').get('src')

        img_url = hemispheres_url + src 
        dictionary={"hemisphere_title": hemisphere_title,"img_url":img_url}
        hemisphere_img_url.append(dictionary) 

    # Mars 
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "fact_table": mars_html_table,
        "mars_hemisphere_images": hemisphere_img_url
    }

    return mars_dict