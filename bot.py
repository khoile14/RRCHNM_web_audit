import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
from datetime import datetime
from urllib.parse import urlparse

class Bot:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors')
        self.browser = webdriver.Chrome(options=chrome_options)

    def check_link(self, link):
        try:
            response = requests.get(link, allow_redirects=True)
            if response.status_code <= 399:
                print(f"The link {link} is working.")
                return "working"
            else:
                print(f"The link {link} returned a status code: {response.status_code}")
                return f"status code: {response.status_code}"
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while checking the link {link}: {e}")
            return f"error: {e}"
        
    def run(self, starting_link, output_file):
        self.browser.get(starting_link)
        if starting_link == "https://rrchnm.org/essays/":
            main_a_elements = self.browser.find_elements(By.CSS_SELECTOR, "#qodef-page-content.qodef-grid.qodef-layout--template a")
        elif starting_link == "https://rrchnm.org/our-work/":
            main_a_elements = self.browser.find_elements(By.CSS_SELECTOR, "#qodef-page-content > div > div > div > section.elementor-section.elementor-top-section.elementor-element.elementor-element-dd98d8f.elementor-section-full_width.elementor-section-height-default.elementor-section-height-default.qodef-elementor-content-no > div > div > div > div > div > div > div.qodef-grid-inner.clear a")
        
        main_links = []

        for a in main_a_elements:
            mainLink = {}
            if(starting_link == "https://rrchnm.org/essays/"):
                mainLink['href'] = a.get_attribute('href')
                mainLink['title'] = a.get_attribute('innerText')
            elif(starting_link == "https://rrchnm.org/our-work/"):
                if(a.get_attribute('class') == 'qodef-e-title-link'):
                    mainLink['href'] = a.get_attribute('href')
                    mainLink['title'] = a.get_attribute('innerText')
                else:
                    continue
            main_links.append(mainLink)
        self.process_links(main_links, output_file, starting_link)

    def process_links(self, main_links, output_file, starting_link):
        with open(output_file, 'w', newline='', encoding= 'utf-8') as file:
            
            writer = csv.writer(file)
            writer.writerow(["Title", "Main Link", "Sub Link", "Status"])

            for link in main_links:
                main_link_href = link["href"]
                main_link_title = link["title"]
                if not main_link_href:
                    continue  # Skip link without href
                
                self.browser.get(main_link_href)
                container_elements = []
                if(starting_link == "https://rrchnm.org/essays/"):
                    container_elements = self.browser.find_elements(By.CSS_SELECTOR, "div[data-widget_type='text-editor.default'] a")
                elif(starting_link == "https://rrchnm.org/our-work/"):
                    container_elements = self.browser.find_elements(By.CSS_SELECTOR, "#qodef-page-content > div > div > div > article > div > div > div > div.qodef-grid-item.qodef-col--4.qodef-ps-info-sticky-holder > div.qodef-portfolio-info > div.qodef-e.qodef-info--info-items > a")
            
                for link_element in container_elements:

                    container_link_href = link_element.get_attribute('href')

                    if not container_link_href:
                        continue  # Skip link without href
                    
                    writer.writerow([main_link_title, main_link_href, container_link_href, self.check_link(container_link_href)])  # Write link to CSV file
                    self.check_link(container_link_href)



bot = Bot()
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
filename = f"output_{timestamp}.csv"

#bot.run("https://rrchnm.org/our-work/", filename)
bot.run("https://rrchnm.org/essays/", filename)
