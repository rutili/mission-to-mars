import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {"executable_path": ChromeDriverManager().install()}

def scrape():
    browser = Browser("chrome", **executable_path, headless=False)
    title,paragraph=news(browser)

    return {
        'title': title,
        'paragraph':paragraph,
        'image':image(browser),
        'facts':facts(),
        'hemispheres':hemispheres(browser)
    }
    
# ### NASA Mars News
def news(browser):
    browser.visit('https://redplanetscience.com/')
    return browser.find_by_css('div.content_title').text, browser.find_by_css('div.article_teaser_body').text

# ### JPL Mars Space Images - Featured Image
def image(browser):
    browser.visit('https://spaceimages-mars.com/')
    browser.links.find_by_partial_text('FULL IMAGE').click()
    return browser.find_by_css('img.fancybox-image')['src']

# ### Mars Facts
def facts():
    return pd.read_html('https://galaxyfacts-mars.com/',header=0)[0].to_html()

# ### Mars Hemispheres
def hemispheres(browser):
    browser.visit('https://marshemispheres.com/')
    hemispheres=[]

    for i in range(4):
        hemisphere = {}
        hemisphere['title'] = browser.find_by_css('a.itemLink h3')[i].text
        browser.find_by_css('a.itemLink h3')[i].click()
        hemisphere['url'] = browser.find_by_text('Sample')['href']
        hemispheres.append(hemisphere)
        browser.back()
    browser.quit()
    return hemispheres