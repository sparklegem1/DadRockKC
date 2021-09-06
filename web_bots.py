from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException



############################### API DESCRIPTION ###################################
# Get all information about local shows from one site with the local gig api
# Employing web scraping to get show information from local sites to provide
# up to date info on local shows




class KnuckleHeadScraper:


    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def get_shows(self):
        import time
        show_info = []

        self.driver.get('https://knuckleheadskc.com/')
        time.sleep(5)

        upcoming_shows = self.driver.find_element_by_xpath('//*[@id="navTopLevel"]/li[2]/a')
        upcoming_shows.click()
        time.sleep(5)


        all_shows = self.driver.find_elements_by_class_name('pl-item')

        for element in all_shows[:11]:
            individual_show = {}
            title = element.find_element_by_class_name('pl-event-link').text
            print(title)
            date = f"{element.find_element_by_class_name('pl-weekday').text}/" \
                   f"{element.find_element_by_class_name('pl-monthday').text}/" \
                   f"{element.find_element_by_class_name('pl-month').text}"
            time = element.find_element_by_class_name('show-end-time-0').text

            try:
                price = element.find_element_by_class_name('pl-sale-status').text

            except NoSuchElementException:
                # import time
                price = element.find_element_by_class_name('buy-tickets').text
                # ticket_button.click()
                # time.sleep(2)
                # price = element.find_element_by_class_name('price-cell').text


            individual_show['title'] = title
            individual_show['date'] = date
            individual_show['time'] = time
            if price == 'BUY TICKETS':
                price = 'Not Free'
            individual_show['price'] = price
            show_info.append(individual_show)
        print(show_info)



