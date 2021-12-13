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
    
    # Mars 
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "fact_table": mars_html_table,
        # "image_tile": image_title,
        # "hemisphere_images": image_list
    }

    return mars_dict