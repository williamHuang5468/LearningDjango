from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Chrome('chromedriver_win32/chromedriver.exe')
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_case(self):
		self.browser.get('http://localhost:8000')
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
		self.check_text_in_table('1: Buy peacock feathers')

		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)
		self.check_text_in_table('1: Buy peacock feathers')
		self.check_text_in_table('2: Use peacock feathers to make a fly')

		self.fail('End the test')

	def check_text_in_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(
			row_text, [row.text for row in rows]
		)


if __name__ == '__main__':
	unittest.main(warnings='ignore')