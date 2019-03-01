#Import dependencies
from bs4 import BeautifulSoup
import pymongo
from splinter import Browser
import requests
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    #visit url
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #pull html text and parse
    html_code = browser.html
    soup = BeautifulSoup(html_code, "html.parser")

    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text

    print(news_title)
    print(news_p)


    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    browser.click_link_by_partial_text("FULL IMAGE")
    #Move to the next image
    actions = ActionChains(browser.driver)
    time.sleep(4)
    actions.send_keys(Keys.ARROW_RIGHT)
    actions.perform()
    time.sleep(5)
    browser.click_link_by_partial_text("more info")
    time.sleep(3)
    browser.click_link_by_partial_href("spaceimages/images/largesize")
    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    featured_image_url  = soup.img['src']

    print(featured_image_url)

    mars_weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather_url)

    mars_weather_html = browser.html
    soup = BeautifulSoup(mars_weather_html, "html.parser")

    tweets = soup.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")

    #Loop through Twitter account to find the most recent post related to Mars weather
    for tweet in tweets:
        try:
            # Identify tweet text
            mars_weather = str(tweet.text)

            # Run only if tweet text starts with "Sol"
            if (mars_weather.startswith('Sol')):
                # Print results
                print(mars_weather)
                break
            else:
                continue


        except Exception as e:
            print(e)

    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)

    facts_html = browser.html
    soup = BeautifulSoup(facts_html, "html.parser")

    mars_table = soup.find("table", class_="tablepress tablepress-id-mars")
    mars_facts = mars_table.find_all('tr')

    key = []
    value = []

    #Loop to append all table data into Key and Value lists
    for row in mars_facts:
        table_data = row.find_all('td')
        key.append(table_data[0].text)
        value.append(table_data[1].text)

    mars_df = pd.DataFrame({
        "Property": key,
        "Value": value
    })

    mars_df

    #Convert into HTML
    mars_facts_html = mars_df.to_html(header = False, index = False)
    mars_facts_html

    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)

    hemispheres_html = browser.html
    soup = BeautifulSoup(hemispheres_html, "html.parser")

    mars_hemispheres = soup.find_all("h3")

    hemisphere_image_urls = []

    #Loop to scrap all hemispheres
    for row in mars_hemispheres:
        title = row.text
        browser.click_link_by_partial_text(title)
        time.sleep(3)
        
        img_html = browser.html
        soup_h = BeautifulSoup(img_html, "html.parser")
        
        url_img = soup_h.find("div", class_="downloads").a["href"]
        
        img_dict = {}
        img_dict["title"] = title
        img_dict["img_url"] = url_img

        hemisphere_image_urls.append(img_dict)
        
        browser.visit(hemispheres_url)

    #Save all the scraped data in a dictionary
    mars_data = {
        "name": "Mars",
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts_html,
        "hemisphere_images": hemisphere_image_urls
    }

    browser.quit()
    return mars_data