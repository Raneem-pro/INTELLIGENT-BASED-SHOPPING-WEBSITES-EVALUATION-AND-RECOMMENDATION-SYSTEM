
from selenium import webdriver
from Screenshot import Screenshot_Clipping

def capture(url):
    ob=Screenshot_Clipping.Screenshot()
    driver=webdriver.Chrome('/Users/rneemalqarni/Documents/chromedriver')
    driver.get(url)
    img_url=ob.full_Screenshot(driver, save_path=r'.', image_name='Myimage.png')
#    print(img_url)
    driver.close()
    driver.quit()
    return img_url
