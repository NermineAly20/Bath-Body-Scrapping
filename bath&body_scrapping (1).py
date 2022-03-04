from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from openpyxl import Workbook
import sys
import urllib.request
import cgi
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

headers={'User-Agent':user_agent,} 
data = dict({'sku': [], 'image': [], 'title': [], 'discount': [], 'price': [], 'current_price': [], 'description': []})
url = "https://www.bathandbodyworks.com.sa/ar/shop-body-care/bath-shower/all-bath-shower/"
driver = webdriver.Chrome()
driver.get(url)
try:
    x=driver.find_element(By.CSS_SELECTOR, "span.exponea-subbox-close")
    x.click()
    print("YEsssssssssss")
except:
    print("No")


while(True):
    try:
        driver.find_element(By.CSS_SELECTOR, "#plp-hits ul li:nth-child(2) .button").click()
    except:
      break


product = driver.find_elements(By.CLASS_NAME, 'field__items')
print(len(product))

#get urls of each product to open
for prodindex in range(0,len(product)):
    pindex = "bb" + str(prodindex + 1)
    producturls = product[prodindex].find_element(By.CLASS_NAME, 'product-selected-url')   
    product_url= producturls.get_attribute("href")
    print(product_url)
    driver_product = webdriver.Chrome()
    driver_product.get(product_url)
    try:
        x=driver_product.find_element(By.CSS_SELECTOR, "span.exponea-subbox-close")
        x.click()
        print("YEsssssssssss")
    except:
       print("No")
    try:
        more = driver_product.find_element(By.CSS_SELECTOR,'span.read-more-description-link')
        more.click()
        #wait = WebDriverWait(driver, 10)
        #wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.read-more-description-link'))).click()
        dis = driver_product.find_elements(By.CSS_SELECTOR,'.content--description .field__content .desc-wrapper .desc-value')
        close = driver_product.find_element(By.CSS_SELECTOR,'span.close')
        data['description'].append(dis[1].text)

    except:
        dis = ""
        data['description'].append(dis)

    # close.click()

    img_product = driver_product.find_element(By.CSS_SELECTOR ,'.img-wrap img')
    image_url = img_product.get_attribute('src')
    print(image_url)
    request=urllib.request.Request(image_url,None,headers) #The assembled request
    response = urllib.request.urlopen(request)
    galleryimg = response.read()
    # print(image)
    imagename = str(pindex) + ".jpg"
    with open(imagename , "wb") as file:
        file.write(galleryimg)

    title =driver_product.find_element(By.CSS_SELECTOR,'.content__title_wrapper h1')
    print(title.text)
    price = driver_product.find_element(By.CLASS_NAME,'price-amount')
    
    
    data['sku'].append(pindex)
    data['image'].append(imagename)
    data['title'].append(title.text)
    data['current_price'].append(price.text)
    driver_product.close()


# print(data['image'])
df = pd.DataFrame(data, columns= ['sku', 'image', 'title', 'description', 'current_price'])
df.set_index('sku')
df.rename(columns= {'sku': 'رمز المنتج (SKU)','image': 'الصور', 'title': 'الأسم', 'description': 'الوصف', 'current_price': 'سعر الشراء'}, inplace=True)

# print(df)
df.to_excel("wearable" + '.xlsx', index = False, header=True)

