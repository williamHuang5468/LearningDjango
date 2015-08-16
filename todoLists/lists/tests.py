from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home
# Create your tests here.

class simpleTest(TestCase):
	def test_url(self):
		homePage = resolve('/')
		self.assertEqual(homePage.func, home)

	def test_response_html(self):
		# create HttpRequest object.	
		request = HttpRequest()
		# Pass request to browser
		response = home(request)
		# assert the content
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)

	def test_save_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new item'

		response = home(request)
		self.assertIn('A new item', response.content.decode())

		expected_html = render_to_string(
			'home.html',
			{'new_item_text': 'A new item'}
		)
		self.assertEqual(response.content.decode(), expected_html)