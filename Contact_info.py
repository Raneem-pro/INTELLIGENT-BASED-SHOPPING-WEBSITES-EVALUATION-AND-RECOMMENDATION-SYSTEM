
from bs4 import BeautifulSoup
import requests




#class Render(QWebEngineView):
#    def __init__(self, url):
#        self.html = None
#        self.app = QApplication(sys.argv)
#        QWebEngineView.__init__(self)
#        self.loadFinished.connect(self._loadFinished)
 #       self.load(QUrl(url))
  #      self.app.exec_()

   # def _loadFinished(self, result):
    #    self.page().toHtml(self.callable)

    #def callable(self, data):
     #   self.html = data
      #  self.app.quit()

import re
def contact(url):
    #html_source = Render(url).html
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    #html_source = soup.find_all('meta')
    
    mail_list = soup.find_all('\w+@\w+\.{1}\w+')
    insta = soup.find_all('(?<!\\w)(?:http(?:s)?:\\/\\/)?(?:(?:www\\.)?(?:instagram\\.com|instagr\\.am)\\/)([a-z0–9_.]{2,30})(?![a-z0–9_.])(?:/)?' )
    linked = soup.find_all('(?<!\\w)(?:http(?:s)?:\\/\\/)?(?:(?:[a-z]+\\.)?linkedin\\.com\\/in\\/)([a-z0–9\\-_%]{2,60})(?![a-z0–9\\-_%])(?:/)?')
    twitter = soup.find_all('(?<!\\w)(?:http(?:s)?:\\/\\/)?(?:www.)?(?:twitter.com)\\/(?!(?:oauth|account|tos|privacy|signup|home|hashtag|search|login|widgets|i|settings|start|share|intent|oct)(?:[\\\'\\"\\?\\.\\/]|$))([a-z0-9_]{1,15})(?![a-z0-9_])(?:/)?')
    face = soup.find_all('(?<!\\w)(?:http(?:s)?:\\/\\/)?(?:www.)?(?:facebook.com|fb.com)\\/(?!(?:rsrc\\.php|apps|groups|events|l\\.php|friends|images|photo.php|chat|ajax|dyi|common|policies|login|recover|reg|help|security|messages|marketplace|pages|live|bookmarks|games|fundraisers|saved|gaming|salesgroups|jobs|people|ads|ad_campaign|weather|offers|recommendations|crisisresponse|onthisday|developers|settings|connect|business|plugins|intern|sharer)(?:[\\\'\\"\\?\\.\\/]|$))(profile\\.php\\?id\\=[0-9]{3,20}|(?!profile\\.php)[a-z0-9\\.]{5,51})(?![a-z0-9\\.])(?:/)?')

    contact_info = 0
    if mail_list != None or insta != None or linked != None or twitter != None or face != None:
      contact_info = 1
      
    return contact_info
      #print ("yes")
  
    #print("mail",mail_list , "\nface", face, "\ninsta", insta, "\nlinked", linked, "twitter",twitter)


#print(contact('https://www.shein.com/'))
#soup = BeautifulSoup(html_source, 'html.parser')

#url ='https://www.nexmo.com/products/sms' #('https://www.next.sa/ar') 'https://www.amazon.com/' 
#html_source = Render(url).html
#soup = BeautifulSoup(html_source, 'html.parser')
#print(soup.find_all('dropdown-row'))
#for name_list in soup.find_all(class_='dropdown-row'):
#    print("11111")
#    print(name_list.text)
    
#browser = webdriver.Chrome('/Users/asmaahakami/Documents/chromedriver')
#url = ('https://www.next.sa/ar')
#browser.get(url)
#html_source = browser.page_source
#browser.quit()
#soup = BeautifulSoup(html_source, 'html.parser')
#print(soup.find_all(class_ ='languageSelectorDropdown'))
#for name_list in soup.find_all(class_ ='dropdown-row'):
#    print("1111")
#    print(name_list.text)
#print("AAAaa")
#List<WebElement>
#driver = requests.get('https://www.next.sa/ar')
#options = driver.find_elements(By.XPATH, '//language')
#options = driver.findElements(
#    By.xpath("//*[@id="+vehicleTypeName+"]/option"))

#List<String>
#text = [] #new ArrayList<>();

#for i in range (1, options.size()):
#    text.add(options.get(i).getText())

#print(text.size)

#label=driver.findElement(By.id("Language"))
#labelSelector = new Select(label)
#labelSelector.deselectByValue("");
#List<WebElement> allOptions =  labelSelector.getOptions()
