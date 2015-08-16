from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home
from lists.models import Item
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

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item')

		self.assertIn('A new item', response.content.decode())
		expected_html = render_to_string(
			'home.html',
			{'new_item_text': 'A new item'}
		)
		self.assertEqual(response.content.decode(), expected_html)

	def test_home_only_save(self):
		request = HttpRequest()
		home(request)
		self.assertEqual(Item.objects.count(), 0)

class ItemModelTest(TestCase):

	def test_save_item(self):
		# add item1
		item1 = Item()
		item1.text = "First item"
		item1.save()
		# add item2
		item2 = Item()
		item2.text = "Second item"
		item2.save()
		# check item of saved.
		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)
		# check item of saved is correct.
		item1 = saved_items[0]
		item2 = saved_items[1]
		self.assertEqual(item1.text, "First item")
		self.assertEqual(item2.text, "Second item")

