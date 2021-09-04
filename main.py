from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
import selenium
# from flask_ckeditor import CKEditor
# from datetime import date
# from functools import wraps
# from flask import abort
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import relationship
# from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
# from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
# from flask_gravatar import Gravatar
# from datetime import datetime
# import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager





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
            title = element.find_element_by_class_name('pl-event-link')
            date = f"{element.find_element_by_class_name('pl-weekday').text}/" \
                   f"{element.find_element_by_class_name('pl-monthday').text}/" \
                   f"{element.find_element_by_class_name('pl-month').text}"
            time = element.find_element_by_class_name('show-end-time').text
            price = element.find_element_by_class_name('pl-sale-status').text
            individual_show['title'] = title
            individual_show['date'] = date
            individual_show['time'] = time
            individual_show['price'] = price

            show_info.append(individual_show)
        print(show_info)



kucklehead_scraper = KnuckleHeadScraper()
kucklehead_scraper.get_shows()