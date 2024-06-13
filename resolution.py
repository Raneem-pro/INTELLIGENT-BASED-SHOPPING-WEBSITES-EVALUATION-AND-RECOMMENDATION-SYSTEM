from bs4 import BeautifulSoup
import requests

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import urllib.request, json

def resolution(new_url):
    url_new = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url='+ new_url +'&strategy=desktop&locale=en'

#url = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://www.next.sa/ar&strategy=desktop&locale=en'
    response = urllib.request.urlopen(url_new)

    data = json.loads(response.read())

    #if data.status_code == 429:
     #   raise TooManyRequests()
    optimized_images_score = data["lighthouseResult"]["audits"]["uses-optimized-images"]["score"]
    webp_images_score = data["lighthouseResult"]["audits"]["uses-webp-images"]["score"]
    #print(optimized_images_score)
    #print(webp_images_score)

    sumdiv = (optimized_images_score + webp_images_score) / 2
    #res = ''
    if sumdiv > 0.79 and sumdiv < 1:
        return 0
    elif sumdiv > 59 and sumdiv < 0.8:
        return 1
    elif sumdiv > 0.39 and sumdiv < 0.6:
        return 2
    elif sumdiv > 0.19 and sumdiv < 0.4:
        return 3
    else:
        return 4


#url = 'https://www.shein.com'
#r = requests.get('https://webspeedtest.cloudinary.com', url)
#response = urllib.request.urlopen('https://webspeedtest.cloudinary.com')
#r = requests.get(response,url)
#print(r.text)

#url = 'http://www.webpagetest.org/runtest.php?url=ghttps://www.lacoste.com/sa/en&runs=1&f=xml&k=<your-api-key>'
#r = urllib.request.urlopen(url)

#print(r)


