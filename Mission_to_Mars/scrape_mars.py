from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
from selenium import webdriver
import time 
import json
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd 

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless = False)

#SCRAPING FOR LATEST HEADLINES

    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    mars_site = bs(html, 'html.parser')
    results = mars_site.find_all('div', class_='list_text')

    dates = []
    titles = []
    descriptions = []

    for result in results:
        date = result.find('div', class_='list_date').text
        dates.append(date)
        title = result.find('div', class_='content_title').text
        titles.append(title)
        description = result.find('div', class_='article_teaser_body').text
        descriptions.append(description)

    #DATA FOR LATEST MARS NEWS    
    newest_date = dates[0]
    newest_title = titles[0]
    newest_description = descriptions[0]
   

#SCRAPING FOR FEATURED IMAGE

    img_url = 'https://spaceimages-mars.com/'
    browser.visit(img_url)
    img_html = browser.html
    mars_images = bs(img_html, 'html.parser')
    #FEATURED IMAGE URL
    featured_image_url = img_url+ mars_images.find('img', class_='headerimage fade-in')['src']
   
    
#SCRAPING FOR MARS TABLE 

    mars_table_url = 'https://galaxyfacts-mars.com/'
    mars_tables = pd.read_html(mars_table_url)
    mars_df = mars_tables[0]
    mars_df = mars_df.rename(columns = {0:'Facts', 1:'Mars', 2: 'Earth'})
    mars_df = mars_df.drop(["Earth"], axis=1)
    mars_df = mars_df.drop([0])
    mars_df = mars_df.reset_index(drop=True)

    mars_table = mars_df.to_html()
    mars_table = mars_table.replace('\n', '')

    hemisphere_dict = {"Cerberus Hemisphere" :'https://marshemispheres.com/cerberus.html', 
    "Schiaparelli Hemisphere":'https://marshemispheres.com/schiaparelli.html', 
    "Syrtis Major Hemisphere":'https://marshemispheres.com/syrtis.html', 
    "Valles Marineris Hemisphere":'https://marshemispheres.com/valles.html',}


    hemisphere_image_urls = []

    for key,value in hemisphere_dict.items():
        browser.visit(value)
        time.sleep(2)
        astro_html = browser.html
        astro_image = bs(astro_html, 'html.parser')
        astros = astro_image.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({title:key, img_url:'https://marshemispheres.com/'+astros})
    
    mars_data = {"newest_title":newest_title, 
                 "newest_date":newest_date, 
                 "newest_description":newest_description,
                 "featured_image_url":featured_image_url, 
                 "mars_table":mars_table, 
                 "hemisphere_image_urls":hemisphere_image_urls}

    browser.quit()

    return mars_data
