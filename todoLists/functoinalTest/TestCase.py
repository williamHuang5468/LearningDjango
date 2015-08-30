from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
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
        #self.browser.get('http://localhost:8000')
        self.assertIn('hello', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('hello', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a To-Do item'
        )

        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_text_in_table('1: Buy peacock feathers')

        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        self.check_text_in_table('1:Buy peacock feathers')
        self.check_text_in_table('2:Use peacock feathers to make a fly')

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)
        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)
        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

    def check_text_in_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(
            row_text, [row.text for row in rows]
        )

if __name__ == '__main__':
    unittest.main(warnings='ignore')
