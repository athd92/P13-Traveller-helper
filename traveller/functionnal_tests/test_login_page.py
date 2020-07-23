from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from main.models import *
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time
import os


class TestFunctionnals(StaticLiveServerTestCase):
    """
    Class used to test the login page
    """

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()
    
    def test_posts_page(self):
        self.driver.get('http://64.227.45.135/')
        self.driver.set_window_size(1920, 1080)
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        time.sleep(1)     
        self.driver.find_element(By.ID, "id_username").click()        
        self.driver.find_element(By.ID, "id_username").send_keys("####")
        self.driver.find_element(By.ID, "id_password").send_keys("####")
        self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)        
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Travelerer Helper").click()
        for i in range(2):
            time.sleep(1)
            self.driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/span/a[1]').click()
        self.driver.find_element(By.ID, "exampleFormControlSelect1").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div[1]/div/a").click()
        self.assertTrue(self.driver.find_element(By.XPATH, '//*[@id="getinfos"]').text, 'Create post')
        self.driver.close()

    def test_open_modal(self):
        self.driver.get('http://64.227.45.135/')
        self.driver.set_window_size(1920, 1080)
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        time.sleep(1)        
        self.driver.find_element(By.ID, "id_username").click()
        time.sleep(1)        
        #login
        self.driver.find_element(By.ID, "id_username").send_keys("#####")
        self.driver.find_element(By.ID, "id_password").send_keys("######")
        self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)        
       
        time.sleep(1)
        for i in range(2):
            time.sleep(1)
            self.driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/span/a[1]').click()
        self.driver.find_element(By.ID, "exampleFormControlSelect1").click()
        self.driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div[1]/div/a").click()
        #open modal
        self.assertTrue(self.driver.find_element(By.XPATH, '//*[@id="getinfos"]').text, 'Create post')
        self.driver.find_element(By.ID, 'getinfos').click()
        #insert datas in modal form
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/form/div[1]/div[1]/input').send_keys("Lyon")
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/form/div[2]/div/input').send_keys("Photographie")
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/form/div[3]/div[1]/input').send_keys("Photographie/ Photos")
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/form/div[3]/div[2]/input').send_keys("25 euros")
        self.driver.find_element(By.XPATH, '//*[@id="total"]').send_keys("1")
        self.driver.find_element(By.XPATH, '//*[@id="wanted"]').send_keys("3")
        self.driver.find_element(By.XPATH, '//*[@id="free"]').send_keys("2")
        self.driver.find_element(By.XPATH, '//*[@id="message"]').send_keys("Lorem ipsum")
        self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/form/button[2]').click()
        time.sleep(3)
        #open modal
        self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[2]/div/div/div[3]/div/a').click()
        # confirm delete
        self.driver.find_element(By.XPATH, '//*[@id="del-post"]').click()

        
