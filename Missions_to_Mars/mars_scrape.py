# Dependencies
from bs4 import BeautifulSoup as bs 
from splinter import Browser
import time
import os
import requests
import pandas as pd

def scrape():
    # Define Path
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Visit Mars News URL to scrape and collect lastest News title and paragraph text
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

    soup.find('div', class_='list_image').find('img')['src']

    # # JPL Mars Space Images - Featured Image
    # Visit Mars News URL to scrap and collect featured image
    url='https://www.jpl.nasa.gov'
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured_image_url)
   
    html = browser.html
    soup = bs(html, 'html.parser')
    time.sleep(2)

    image_link = soup.find('a', id= 'full_image')['data-fancybox-href']  
    # Concatenate website url with scrapped route
    featured_image_url = url + image_link
    featured_image_url

    # Visit Mars facts URL to scrape
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)

    # Use Pandas to "read_html" to parse the URL
    tables = pd.read_html(facts_url)
    tables
    # Make tables with Mars facts into a Dataframe
    table = tables[0]
    table.columns = ['Description', 'Mars']
    table
    # Convert mars-df into a html table
    html_table = table.to_html()
    html_table

    usgs_url = 'https://astrogeology.usgs.gov'
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    hemispheres_soup = bs(hemispheres_html, 'html.parser')
    time.sleep(1)
    #iterate through each hemisphere data
    for x in range(4):
    #html object
        html = browser.html
    #Parse HTML with Beautiful Soup
        images_soup = bs(html, 'html.parser')
        mars_hemispheres = images_soup.find('div', class_='collapsible results')
        mars_hemispheres_1 = mars_hemispheres.find_all('div', class_='item')
        hems_image_urls = []
        
    for mar in mars_hemispheres_1:
        # Collect Title
        m_hems = mar.find('div', class_='description')
        title = m_hems.h3.text
        
        # Collect image link by browsing to hemisphere page
        hemisphere_link = m_hems.a['href']
        browser.visit(usgs_url + hemisphere_link)
        
        image_html = browser.html
        image_soup = bs(image_html, 'html.parser')
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']
        
        # Create Dictionary to store title and url info
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url
        hems_image_urls.append(image_dict)
        
    print(hems_image_urls)
                
    m_dict ={
            'news_title': news_title,
            'news_': news_paragraph,
            'featured_image_url': featured_image_url,
            'fact_table': str(html_table),
            'hemisphere_images': hems_image_urls
        }
    m_dict

    browser.quit()

    return m_dict
  
    

