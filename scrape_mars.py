# Import dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import time
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

# Start up manager and open Chrome
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)
#------------------------------------------------------------------------------------------------

def scrape():
    browser = init_browser()

# Finding the latest article
# Visit the webpage

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = bs(html,'html')

    title = soup.find_all('div', class_ ="content_title")[1].text
    description = soup.find('div', class_ ="article_teaser_body").text
    #-------------------------------------------------------------------------------------------------

    # Searches for featured images.
    # Visit the webpage

    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    time.sleep(1)

    html = browser.html
    soup = bs(html,'html')

    browser.find_by_tag('footer').click()
    time.sleep(2)
    browser.links.find_by_partial_text('more info').click()
    element = browser.find_by_tag('figure')
    figure = element.find_by_tag('a')
    featured_img_url = figure['href']
    #----------------------------------------------------------------------------------------------------

    # Searches for the table.
    # Visit the webpage

    url3 = "https://space-facts.com/mars/"
    table = pd.read_html(url3)
    df = table[0]
    df.columns = ["","Mars"]
    df.set_index("", inplace = True)

    table = df.to_html()

    #-----------------------------------------------------------------------------------------------------

    # Searches for the hemisphere images.
    # Visit the webpage

    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)
    html = browser.html
    soup = bs(html,'html')

    hemispheres = soup.find_all('div', class_ = 'description')
    hemilen = len(hemispheres)
    browser.find_by_tag("h3").click()
    mars = []

    for x in range(1,hemilen+1):
        wide = browser.find_by_id("wide-image")
        img = wide.find_by_tag('img')
        image = img[1]['src']
        
        mars.append(image)
        time.sleep(2)
        browser.back()
        
        try:
            browser.find_by_tag("h3")[x].click()
        except:
            print('done')

    mars_list = [
        {'title':'Cerberus Hemisphere', "image": mars[0]},
        {'title':'Schiaparelli Hemisphere', "image": mars[1]},
        {'title':'Syrtis Major Hemisphere', "image": mars[2]},
        {'title':'Valles Marineris Hemisphere Hemisphere', "image": mars[3]}
    ]
    
    m_dict={
        'featured_url':featured_img_url,
        'feature_title':title,
        'feature_description':description,
        'table1': table,
        'hemi1': mars_list[0],
        'hemi2': mars_list[1],
        'hemi3': mars_list[2],
        'hemi4': mars_list[3]
        }

        

    # Closes out the browser.
    browser.quit()
    return m_dict 