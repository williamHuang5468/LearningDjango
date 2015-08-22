from django.test import LiveServerTestCase
from selenium import webdriver
import unittest
import os


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        path = os.path.dirname(
            os.path.abspath(__file__)) + "\chromedriver_win32\chromedriver.exe"
        self.browser = webdriver.Chrome(path)
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_list(self):
        self.browser.get(self.live_server_url)

if __name__ == '__main__':
    unittest.main(warnings='ignore')
