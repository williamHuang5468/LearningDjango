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

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_element_by_tag_name('tr')
		self.assertTrue(
			#rows.text == '1: Buy peacock feathers', "New to-do item did not appear in table -- its text was:\n%s" % (
			#table.text)
			'1: Buy peacock feathers', [row.text for row in rows]
		)
		self.assertTrue(
			'2: Use peacock feathers to make a fly', [row.text for row in rows]
		)
		'''
		about `for row in rows` is fail, because the rows is webelement, it can't be iterative.
		any sound like the iterative method.

		self.assertTrue(
			any(row.text == '1: Buy peacock feathers' for row in rows),
			"New to-do item did not appear in table -- its text was:\n%s" % (
			table.text,
			)
		)
		'''
		self.fail('End the test')


if __name__ == '__main__':
	unittest.main(warnings='ignore')