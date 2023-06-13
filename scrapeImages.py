import requests
import os
from bs4 import BeautifulSoup as bs
import logging
import configparser
import yagmail





config = configparser.ConfigParser()
config.read("python automation/config.ini")
password = config.get("email_password", "password")



# create a server connection with smtplib server
yag = yagmail.SMTP("mfonekpo34@gmail.com", password)


# configure the log file to keep track of the scraping
logging.basicConfig(filename="scrapeImages.log", level=logging.INFO)

# change to the directory for the image to be saved
os.chdir("python automation/webscraping")
os.makedirs("pictures", exist_ok = True)
os.chdir("pictures")


image_count = 0
url = "https://xkcd.com"

while not  url.endswith("#"):

    logging.info(f"Scraping initiated for url - {url}")


    # request the web page
    res = requests.get(url)


    soup = bs(res.text, "html.parser") #donwload rhe web page


    # get the name tag to get the name of the image
    nameTag = soup.find(id = "ctitle")
    image_name = nameTag.text + ".jpeg"


    # get the image tag
    divTag = soup.find(id = "comic")
    img_tag = divTag.find("img")["src"]
    img_link = "https:" + img_tag


    #save the image downloaded to the images folder
    imageTodownload = requests.get(img_link).content
    with open(image_name, "wb") as file:
        file.write(imageTodownload)
        logging.info(f"Image {image_name} saved")
        image_count += 1



    # navigating to the previous page
    ulTag = soup.find("ul", class_ = "comicNav")
    prevNav = ulTag.select("a")
    url = "https://xkcd.com" + prevNav[1]["href"]


else:
    print("Scraping completed...")
    logging.info(f"Scraping completed for url - {url}")
    logging.info(f"{image_count} images saved")
    yag.send(f"mfonekpo34@gmail.com", "Webscraping done", "done scraping {image_count} the images fromn xkcd.com")
