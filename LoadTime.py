from selenium import webdriver

def loadTime(url):
    driver=webdriver.Chrome('/Users/rneemalqarni/Documents/chromedriver')
    driver.get(url)

    load_time = driver.execute_script(
            """
            var loadTime = ((window.performance.timing.domComplete - window.performance.timing.navigationStart)/1000);
            return loadTime;
            """
            )
    return load_time



