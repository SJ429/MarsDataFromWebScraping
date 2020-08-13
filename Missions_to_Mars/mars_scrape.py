
# Dependencies
from bs4 import BeautifulSoup as bs 
from splinter import Browser
import time
import os
import requests
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Visit Mars News URL to scrap and collect lastest News Title and paragraph text
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    soup.find_all('div', class_='content_title')

    soup.find_all('div', class_='content_title')[1].text

    news_title=soup.find_all('div', class_='content_title')[1].text
    print(news_title)

    soup.find('div', class_='article_teaser_body')

    news_paragraph = soup.find('div', class_='article_teaser_body').text
    print(news_paragraph)


    # JPL Mars Space Images - Featured Image
    #Visit Mars News URL to scrap and collect featured image
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured_image_url)

    #HTML to scrape 
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    time.sleep(2)

    # Retrieve feature-image url 
    image_link = soup.find('a', id= 'full_image')['data-fancybox-href']


    # Website Url 
    url='https://www.jpl.nasa.gov'

    # Concatenate website url with scrapped route
    image_url = url + image_link

    # Display full link to featured image
    image_url

    #Mars Facts
    url = "https://space-facts.com/mars/"
    browser.visit(url)

    # Use Pandas to "read_html" to parse the URL
    tables = pd.read_html(url)
    tables

    #Make tables with Mars Facts into a Dataframe
    table = tables[0]
    table.columns = ['Description', 'Mars']
    table

    #convert mars-df into a html table

    html_table = table.to_html()
    html_table

    # Mars hemisphere Data
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(2)

    # Make list for each hemisphere url 
    hemisphere_image_urls = []

    # Define the beginning of url 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'
    #HTML ObjectObject
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Loop through to get hemisphere data
    for i in items: 
    # Store title
     hemisphere_title = i.find('h3').text
    
    # Store link that leads to full image website
    partial_image_url = i.find('a', class_='itemLink product-item')['href']
    
    # Visit the link that contains the full image website 
    browser.visit(hemispheres_main_url + partial_image_url)
    
    # HTML Object of individual hemisphere information website 
    partial_image_html = browser.html
    
    # Parse HTML with Beautiful Soup for every individual hemisphere information website 
    soup = bs( partial_image_html, 'html.parser')
    
    # Retrieve full image source 
    hemisphere_image_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
    # Append the retreived information into a list of dictionaries 
    hemisphere_image_urls.append({"title" : hemisphere_title, "hemisphere_image" : hemisphere_image_url})
    print(hemisphere_image_urls)
  
    mars_dict={'title': news_title, 
            'paragraph':news_paragraph, 
            'featured_image_url':image_url,
            'table': str(html_table),  
            'df': str(table),
            'hemisphere_title': hemisphere_title,
            'hemispheres_images': hemisphere_image_urls}
        
    return mars_dict