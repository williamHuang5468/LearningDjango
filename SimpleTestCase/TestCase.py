from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.Chrome('chromedriver_win32/chromedriver.exe')
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_case(self):
		self.browser.get('http://localhost:8000')
		self.assertIn('To-Do', self.browser.title)
		#assert 'To-Do' in browser.title, "Browser title was " + browser.title
		self.fail('Finish the test!')

if __name__ == '__main__':
	unittest.main(warnings='ignore')