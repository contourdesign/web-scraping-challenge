# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# init browser
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser("chrome", **executable_path, headless=False)


# Scrape initiated, create dictionary
def scrape():

    final_data = {}

    output = marsNews()
    final_data["mars_news"] = output[0]
    final_data["mars_paragraph"] = output[1]
    final_data["mars_image"] = marsImage()
    final_data["mars_facts"] = marsFacts()
    # final_data["mars_hemisphere"] = marsHem()

    # return output dictionary
    return final_data

# Mars News scrape
def marsNews():
    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text
    output = [news_title, news_p]
    return output

# Mars featured image scrape
def marsImage():
    image_url = "https://spaceimages-mars.com/"
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    image = soup.find("img", class_="headerimage")["src"]
    featured_image_url = "https://spaceimages-mars.com/" + image
    return featured_image_url

# Mars factoids
def marsFacts():
    import pandas as pd
    # facts_url = "https://galaxyfacts-mars.com/"
    # browser.visit(facts_url)
    # mars_data = pd.read_html(facts_url)
    # mars_data = pd.DataFrame(mars_data[0])
    # mars_data.columns = ["Description", "Value"]
    # # mars_data = mars_data.set_index("Description")
    # mars_facts = mars_data.to_html(index = False, header = False)
    # return mars_facts


    facts_url = "https://galaxyfacts-mars.com/"
    browser.visit(facts_url)
    mars_data = pd.read_html(facts_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_facts = mars_data.to_html(header=False, index=False)
    return mars_facts


# Hemispheres
def marsHem():
    import time 
    hemispheres_url = "https://marshemispheres.com/"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_hemisphere = []

    # soupify
    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    # for loop to get hemispheres
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://marshemispheres.com/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        dictionary = {"title": title, "img_url": image_url}
        mars_hemisphere.append(dictionary)

    return mars_hemisphere

    