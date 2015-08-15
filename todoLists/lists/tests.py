from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home
# Create your tests here.

class simpleTest(TestCase):
	def test_url(self):
		homePage = resolve('/')
		self.assertEqual(homePage.func, home)

	def response_html(self):
		# create HttpRequest object.	
		request = HttpRequest()
		# Pass request to browser
		response = home(request)
		# assert the content
		self.assertTrue(response.startswith(b"<html>"))
		self.assertIn(b'<title>hello</title>', response.content)
		self.assertTrue(response.startswith(b"</html>"))