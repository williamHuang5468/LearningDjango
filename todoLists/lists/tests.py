from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home
from lists.models import Item, List


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

    def test_home_only_save(self):
        request = HttpRequest()
        home(request)
        self.assertEqual(Item.objects.count(), 0)

    def display_mutiItems(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        request = HttpRequest()
        response = home(request)

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())


class NewToDoTest(TestCase):

    def test_save_request(self):
        '''
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new item'

        home(request)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item')
        '''

        self.client.post(
            '/lists/new',
            data={'item_text': 'A new item'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item')

    def test_home_redirects(self):
        '''
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new item'

        response = home(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['location'], '/lists/the-only-list-in-the-world/')
        '''
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new item'}
        )
        list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (list.id,))


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list1 = List.objects.create()
        response = self.client.get('/lists/%d/' % (list1.id,))
        self.assertTemplateUsed(response, 'lists.html')

    def test_displays_all_items(self):
        list1 = List.objects.create()
        Item.objects.create(text='itemey 1', list=list1)
        Item.objects.create(text='itemey 2', list=list1)

        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get('/lists/%d/' % (list1.id, ))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)


class ItemAndListModelTest(TestCase):

    def test_save_item(self):
        # add item1
        list1 = List()
        list1.save()

        item1 = Item()
        item1.text = "First item"
        item1.list = list1
        item1.save()
        # add item2
        item2 = Item()
        item2.text = "Second item"
        item2.list = list1
        item2.save()

        save_list = List.objects.first()
        self.assertEqual(save_list, list1)
        # check item of saved.
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        # check item of saved is correct.
        item1 = saved_items[0]
        item2 = saved_items[1]
        self.assertEqual(item1.text, "First item")
        self.assertEqual(item1.list, list1)
        self.assertEqual(item2.text, "Second item")
        self.assertEqual(item2.list, list1)


class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))
