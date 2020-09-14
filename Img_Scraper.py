from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
import requests
import os
from PIL import Image
import io
import hashlib


driver = webdriver.Chrome("===================")#Enter chrome driver path
driver.maximize_window()
driver.get("https://www.google.com")

time.sleep(2)
driver.find_element_by_xpath("//*[@id='tsf']/div[2]/div[1]/div[1]/div/div[2]/input").send_keys("========")#query to search

act=ActionChains(driver)
act.send_keys(Keys.ENTER).perform()
time.sleep(3)

driver.find_element_by_xpath("//*[@id='hdtb-msb-vis']/div[2]/a").click()


#=====================================================================#
max_links_to_fetch="The number of images needs to be download."#enter count of images
image_urls = set()
image_count=0
while image_count<max_links_to_fetch:
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True

    thumbnail_results = driver.find_elements_by_css_selector("img.Q4LuWd")

    for img in thumbnail_results:
    # try to click every thumbnail such that we can get the real image behind it
        try:
            img.click()
            time.sleep(1)
        except Exception:
            continue

        # extract image urls
        actual_images = driver.find_elements_by_css_selector('img.n3VNCb')
        for actual_image in actual_images:
            if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                image_urls.add(actual_image.get_attribute('src'))
                print(image_urls)

                image_count = len(image_urls)
                print(image_count)

        if len(image_urls) >= max_links_to_fetch:
            print(f"Found: {len(image_urls)} image links, done!")
            break

    else:
        print("Found:", len(image_urls), "image links, looking for more ...")
        time.sleep(30)
        load_more_button = driver.find_element_by_css_selector(".mye4qd")
        if load_more_button:
            driver.execute_script("document.querySelector('.mye4qd').click();")



def persist_image(folder_path: str, file_name: str, url: str):
    try:
        image_content = requests.get(i).content

    except Exception as e:
        print(f"ERROR - Could not download {i} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        folder_path = os.path.join(folder_path, query)
        if os.path.exists(folder_path):
            file_path = os.path.join(folder_path, hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        else:
            os.mkdir(folder_path)
            file_path = os.path.join(folder_path, hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {i} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {i} - {e}")

query = "=================="  # change your set of querries here
# images_path = #enter your desired image path
images_path = '================'
for i in image_urls:
    persist_image(images_path, query, i)

print(image_count)
print(image_urls)
print("Bye")