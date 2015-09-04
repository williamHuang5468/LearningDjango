#TDD for First Page

##Write Test Case
```python

    from selenium import webdriver
    
    browser = webdriver.Chrome('chromedriver_win32/chromedriver.exe')
    browser.get('http://localhost:8000')
    
    assert 'Django' in browser.title
```

>> Note: you need to download chromedriver from [ChromeWebDriver](http://selenium-python.readthedocs.org/en/latest/api.html#selenium.webdriver.remote.webdriver.WebDriver "WebDriver") 

## Build Fail 

Run it 

    $ python3 functional_tests.py
    Traceback (most recent call last):
    File "functional_tests.py", line 6, in <module>
    assert 'Django' in browser.title
    AssertionError

## Build the project

`django-admin.py startproject superlists`──

    ├── functional_tests.py
    └── superlists
        ├── manage.py
        └── superlists
            ├── __init__.py
            ├── settings.py
            ├── urls.py
            └── wsgi.py

Run server

    python3 manage.py runserver

run testcase again

    python3 functional_tests.py

##  Using unittest

```Python
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
            self.fail('Finish the test!')
    
    if __name__ == '__main__':
        unittest.main(warnings='ignore')
```

**class need to extends `unittest.TestCase` be a testcase.**

we use `assertIn` to replace `assert`

[unittest Doc](https://docs.python.org/3/library/unittest.html "doc")

### wait time  ###

```Python

    self.browser.implicitly_wait(3)
```

## Do the function ##

create the models.

    python3 manage.py startapp lists

Will get

    superlists/
    ├── db.sqlite3
    ├── functional_tests.py
    ├── lists
    │   ├── admin.py
    │   ├── __init__.py
    │   ├── migrations
    │   │    └── __init__.py
    │   ├── models.py
    │   ├── tests.py
    │   └── views.py
    ├── manage.py
    └── superlists
        ├── __init__.py
        ├── __pycache__
        ├── settings.py
        ├── urls.py
        └── wsgi.py

實作功能

1. 接受Request
1. 處理不同Request
1. 能夠依據Request回傳不同結果

所以我們要作

1. 區別URL "/"和 "/About"
1. Get url , and then return Html

## Write unit test

lists/tests.py

    from django.core.urlresolvers import resolve
    from django.test import TestCase
    from lists.views import home_page 

    class HomePageTest(TestCase):
        def test_root_url_resolves_to_home_page_view(self):
            found = resolve('/') #
            self.assertEqual(found.func, home_page)

python manage.py test

    ImportError: cannot import name 'home_page'

Add url

    urlpatterns = patterns('',
        url(r'^$', 'lists.views.home', name='home'),
    )

## Modify Circle ##

1. Create models
1. Chagne test
1. Using the view 
1. and add the urls
1. final, return the view.

## Using form to send POST requests##

除錯三個方法:
1. 將值Print出來
1. 讓錯誤訊息吐更多資訊
1. 使用time.sleep在執行之前緩慢。

    import time
    time.sleep(10)
    fail()

In `home.html` can add `{% csrf_token %}`to open debug mode.

## Process POST on server ##

用`{{}}`用來拿取Python objcets

作測試可以用render_to_string(page, { 'key', 'value'})送值，將網頁轉為string

**view**

    return render(request, 'home.html', 
        {
            'new_item_text': request.POST['item_text'],
        }
    )

下方程式碼為送POST資料
    
    {
        'new_item_text': request.POST['item_text'],
    }

## Flow ##

View 轉址 

Urls urlMapping

## First Model ##

models 

extends `models.Model`

    python manage.py makemigrations

Model自動產生ID，如果要額外添加屬性，需要在Model中加入

[Property type Doc](https://docs.djangoproject.com/en/1.7/intro/tutorial01/#creating-models)

### new field 等於 new migration ###

if you get the error message

    django.db.utils.OperationalError: table lists_item has no column named text

then, use command

    python manage.py makemigrations

you need give the default value.

    like TextField(default='')

again

    python manage.py makemigrations

### Saving POST to DB ###
    
    Item.objects.create() is same new Item, but don't need save.

migrate

    python manage.py migrate

## -- Todo

## reset the sql

    delete the `db.sqlite3`
    python manage.py migrate --noinput
    
## Move the function test into test.py
    
    create a folder in project folder.(like functional_tests)
    move the testcase into folder.
    create a __init__.py , the testcase will be module.

run 

    python manage.py test functional_tests

run all, include unit test and funcitonal test

    python manage.py test

just run unit test
    
    python manage.py test lists

    
    python manage.py test functional_tests

## Small Design When Necessary

ToDo:

- We want each user to be able to store their own list—at least one, for now.
- A list is made up of several items, whose primary attribute is a bit of descriptive text.
- We need to save lists from one visit to the next. For now, we can give each user a unique URL for their list. Later on we may want some way of automatically recognising users and showing them their lists.

## YAGNI!

    You aint gonna need it!

Think about it why we need it.
Is it necessary?

[https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it](https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it)

## Representational State Transfer (REST)

Each list can have its own URL:

    /lists/<list identifier>/

### Todo

- <s>Get FTs to clean up after themselves</s>
- Adjust model so that items are associated with different lists
- Add unique URLs for each list
- Add a URL for creating a new list via POST
- Add URLs for adding a new item to an existing list via POST

## Implementing the New Design Using TDD

lists/test.py

    self.assertEqual(response.status_code, 302)
    self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')

Running the unit tests gives us an expected fail:

    python manage.py test lists

Fails message:

    AssertionError: '/' != '/lists/the-only-list-in-the-world/'

lists/views.py
    
    ```Python
    def home_page(request):
        if request.method == 'POST':
            Item.objects.create(text=request.POST['item_text'])
            return redirect('/lists/the-only-list-in-the-world/')

        items = Item.objects.all()
        return render(request, 'home.html', {'items': items})
    ```

Get Message

    self.check_for_row_in_list_table('1: Buy peacock feathers')
    [...]
    selenium.common.exceptions.NoSuchElementException: Message: 'Unable to locate
    element: {"method":"id","selector":"id_list_table"}' ; Stacktrace:

## Testing Views, Templates, and URLs Together with the Django Test Client

### A New Test Class

lists.tests.py

    class ListViewTest(TestCase):
        def test_displays_all_items(self):
            Item.objects.create(text='itemey 1')
            Item.objects.create(text='itemey 2')
            
            response = self.client.get('/lists/the-only-list-in-the-world/') #

            self.assertContains(response, 'itemey 1') #
            self.assertContains(response, 'itemey 2') #

Get MSG

    AssertionError: 404 != 200 : Couldn't retrieve content: Response code was 404

### A New URL

Our singleton list URL doesn’t exist yet. We fix that in superlists/urls.py.

lists.urls.py

    urlpatterns = patterns('',
        url(r'^$', 'lists.views.home_page', name='home'),
        url(r'^lists/the-only-list-in-the-world/$', 'lists.views.view_list', name='view_list'),
    # url(r'^admin/', include(admin.site.urls)),
    )

Get MSG

    AttributeError: 'module' object has no attribute 'view_list'
    [...]
    django.core.exceptions.ViewDoesNotExist: Could not import
    lists.views.view_list. View does not exist in module lists.views.

### A New View Function

Let’s create a dummy view function in lists/views.py

lists/views.py

    def view_list(request):
        pass

Get

    ValueError: The view lists.views.view_list didn't return an HttpResponse
    object. It returned None instead.

Change

    def view_list(request):
        items = Item.objects.all()
        return render(request, 'home.html', {'items': items})

Get

    Ran 8 tests in 0.016s
    OK

And the FTs should get a little further on:

    AssertionError: '2: Use peacock feathers to make a fly' not found in ['1: Buy
    peacock feathers']

### A Separate Template for Viewing Lists

Let’s add a new test test to check that it’s using a different template

lists/tests.py

    class ListViewTest(TestCase):
        def test_uses_list_template(self):
            response = self.client.get('/lists/the-only-list-in-the-world/')
            self.assertTemplateUsed(response, 'list.html')

        def test_displays_all_items(self):
            [...]

Get

    AssertionError: False is not true : Template 'list.html' was not a template used to render the response. Actual template(s) used: home.html

Change the view

    def view_list(request):
        items = Item.objects.all()
        return render(request, 'list.html', {'items': items})

Get

    django.template.base.TemplateDoesNotExist: list.html

Let’s create a new file at `lists/templates/list.html`.

Get

    AssertionError: False is not true : Couldn't find 'itemey 1' in response

lists/tempaltes/home.html

    <body>
        <h1>Start a new To-Do list</h1>
        <form method="POST">
            <input name="item_text" id="id_new_item" placeholder="Enter a to-do item" />
            {% csrf_token %}
        </form>
    </body

lists/views.py

    def home_page(request):
        if request.method == 'POST':
            Item.objects.create(text=request.POST['item_text'])
            return redirect('/lists/the-only-list-in-the-world/')

        return render(request, 'home.html')

FT

    AssertionError: '2: Use peacock feathers to make a fly' not found in ['1: Buy peacock feathers']

We can fix that in lists/templates/list.html:

    <form method="POST" action="/">

FT

    self.assertNotEqual(francis_list_url, edith_list_url) AssertionError: 'http://localhost:8081/lists/the-only-list-in-the-world/' == 'http://localhost:8081/lists/the-only-list-in-the-world/'

## Another URL and View for Adding List Items

- <s> Get FTs to clean up after themselves</s>
- Adjust model so that items are associated with different lists
- Add unique URLs for each list
- Add a URL for creating a new list via POST
- Add URLs for adding a new item to an existing list via POST

### A Test Class for New List Creation

Open up lists/tests.py, and move the `test_home_page_can_save_a_POST_request` and `test_home_page_redirects_after_POST` methods into a new class, then change their names:

lists/tests.py

    class NewListTest(TestCase):
        def test_saving_a_POST_request(self):
            request = HttpRequest()
            request.method = 'POST'
            [...]

        def test_redirects_after_POST(self):
            [...]

Change 

lists/tests.py

    class NewListTest(TestCase):
        def test_saving_a_POST_request(self):
            self.client.post(
                '/lists/new',
                data={'item_text': 'A new list item'}
            )

            self.assertEqual(Item.objects.count(), 1)
            new_item = Item.objects.first()
            self.assertEqual(new_item.text, 'A new list item')

        def test_redirects_after_POST(self):
            response = self.client.post(
                '/lists/new',
                data={'item_text': 'A new list item'}
            )

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')

Get
    
    self.assertEqual(Item.objects.count(), 1)
    AssertionError: 0 != 1
    [...]
    self.assertEqual(response.status_code, 302)
    AssertionError: 404 != 302  

The first failure tells us we’re not saving a new item to the database, and the second says that, instead of returning a 302 redirect, our view is returning a 404. That’s because we haven’t built a URL for /lists/new, so the `client.post` is just getting a 404 response.

### A URL and View for New List Creation

Let’s build our new URL now:

lists/urls.py

    urlpatterns = patterns('',
        url(r'^$', 'lists.views.home_page', name='home'),
        url(r'^lists/the-only-list-in-the-world/$', 'lists.views.view_list',
        name='view_list'
        ),
        url(r'^lists/new$', 'lists.views.new_list', name='new_list'),
        # url(r'^admin/', include(admin.site.urls)),
    )

Get

    ViewDoesNotExist

lists/views.py

    def new_list(request):
        pass

    def new_list(request):
        return redirect('/lists/the-only-list-in-the-world/')

Get 

    self.assertEqual(Item.objects.count(), 1)
    AssertionError: 0 != 1 [...]
    AssertionError: 'http://testserver/lists/the-only-list-in-the-world/' != '/lists/the-only-list-in-the-world/'

Change

    def new_list(request):
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world/')

Get

    self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/') 
    AssertionError: 'http://testserver/lists/the-only-list-in-the-world/' != '/lists/the-only-list-in-the-world/'

lists.tests.py
    
    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')

Get
        
    Ran 8 tests in 0.030s
    OK

### Removing Now-Redundant Code and Tests

lists/views.py

    def home(request):
        return render(request, 'home.html')

### Pointing Our Forms at the New URL

lists/templates/home.html, lists/templates/list.html

    <form method="POST" action="/lists/new">

Get

    AssertionError: 'http://localhost:8081/lists/the-only-list-in-the-world/' == 'http://localhost:8081/lists/the-only-list-in-the-world/'

### Now ToDo

- <s>Get FTs to clean up after themselves</s>
- Adjust model so that items are associated with different lists
- Add unique URLs for each list
- <s>Add a URL for creating a new list via POST</s>
- Add URLs for adding a new item to an existing list via POST

## Adjusting Our Models

調整Model，加入List Model

lists/tests.py

    -from lists.models import Item
    +from lists.models import Item, List

    -class ItemModelTest(TestCase):
    +class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
    + list_ = List()
    + list_.save()


    + first_item.list = list_
    first_item.save()

    + second_item.list = list_
    second_item.save()

    + saved_list = List.objects.first()
    + self.assertEqual(saved_list, list_)

    self.assertEqual(first_saved_item.text, 'The first (ever) list item')
    + self.assertEqual(first_saved_item.list, list_)
    self.assertEqual(second_saved_item.text, 'Item the second')
    + self.assertEqual(second_saved_item.list, list_)

We create a new `List` object, and then we assign each item to it by assigning it as
its `.list` property. We check the list is properly saved, and we check that the two items
have also saved their relationship to the list.

Your first error should be:

    ImportError: cannot import name 'List'

你還未定義你的List, 至Models.py 新增一個List的Class

Then

    AttributeError: 'List' object has no attribute 'save'

新增一個Save method

then

    django.db.utils.OperationalError: no such table: lists_list

Run makemigrations:

    python manage.py makemigrations

will get 

    Migrations for 'lists':
        0003_list.py:
            - Create model List

Then 

    self.assertEqual(first_saved_item.list, list_)
    AttributeError: 'Item' object has no attribute 'list'

### A Foreign Key Relationship

lists/models.py

    from django.db import models

    class List(models.Model):
        pass

    class Item(models.Model):
        text = models.TextField(default='')
        list = models.TextField(default='')

run test

    python manage.py test lists

get

    django.db.utils.OperationalError: table lists_item has no column named list

Run 

    python manage.py makemigrations

Get

    Migrations for 'lists':
        0004_item_list.py:
            - Add field list to item

Then 

    AssertionError: 'List object' != <List: List object>

>> We’re not quite there. Look closely at each side of the !=. Django has only saved the string representation of the List object. To save the relationship to the object itself, `we tell Django about the relationship between the two classes using a ForeignKey`:

lists/models.py

    from django.db import models

    class List(models.Model):
        pass

    class Item(models.Model):
        text = models.TextField(default='')
        list = models.ForeignKey(List, default=None)

That’ll need a migration too. Since the last one was a red herring, let’s delete it and replace it with a new one:

    rm lists/migrations/0004_item_list.py
    
    python manage.py makemigrations

Get

    Migrations for 'lists':
        0004_item_list.py:
            - Add field list to item

### Adjusting the Rest of the World to Our New Models

    python manage.py test lists

Get Message

    [...]
    ERROR: test_displays_all_items (lists.tests.ListViewTest)
    django.db.utils.IntegrityError: NOT NULL constraint failed: lists_item.list_id
    [...]
    ERROR: test_redirects_after_POST (lists.tests.NewListTest)
    django.db.utils.IntegrityError: NOT NULL constraint failed: lists_item.list_id
    [...]
    ERROR: test_saving_a_POST_request (lists.tests.NewListTest)
    django.db.utils.IntegrityError: NOT NULL constraint failed: lists_item.list_id
    Ran 7 tests in 0.021s
    FAILED (errors=3)

lists/test.py

    class ListViewTest(TestCase):
        def test_displays_all_items(self):
            list_ = List.objects.create()
            Item.objects.create(text='itemey 1', list=list_)
            Item.objects.create(text='itemey 2', list=list_)

That gets us down to two failing tests, both on tests that try to POST to our new_list
view. Decoding the tracebacks using our usual technique, working back from error, to
line of test code, to the line of our own code that caused the failure, we identify:

[First Time is not appear]

    File "/workspace/superlists/lists/views.py", line 14, in new_list
    Item.objects.create(text=request.POST['item_text'])

[Continue will succuess]

lists/views.py

    from lists.models import Item, List
    [...]
    def new_list(request):
        list_ = List.objects.create()
        Item.objects.create(text=request.POST['item_text'], list=list_)
        return redirect('/lists/the-only-list-in-the-world/')

### Todo

- <s>Get FTs to clean up after themselves</s>
- <s>Adjust model so that items are associated with different lists</s>
- Add unique URLs for each list
- <s>Add a URL for creating a new list via POST</s>
- Add URLs for adding a new item to an existing list via POST

### Each List Should Have Its Own URL

Todo

- <s>Get FTs to clean up after themselves</s>
- <s>Adjust model so that items are associated with different lists</s>
- <b>Add unique URLs for each list</b>
- <s>Add a URL for creating a new list via POST</s>
- Add URLs for adding a new item to an existing list via POST

Let’s change `List
ViewTest` so that the two tests point at new URLs.

在ViewTest修改兩個測試, 針對新的Urls.

lists/test.py

    class ListViewTest(TestCase):
        def test_uses_list_template(self):
            list_ = List.objects.create()
            response = self.client.get('/lists/%d/' % (list_.id,))
            self.assertTemplateUsed(response, 'list.html')
            
        def test_displays_only_items_for_that_list(self):
            correct_list = List.objects.create()
            Item.objects.create(text='itemey 1', list=correct_list)
            Item.objects.create(text='itemey 2', list=correct_list)
            other_list = List.objects.create()
            Item.objects.create(text='other list item 1', list=other_list)
            Item.objects.create(text='other list item 2', list=other_list)

            response = self.client.get('/lists/%d/' % (correct_list.id,))

            self.assertContains(response, 'itemey 1')
            self.assertContains(response, 'itemey 2')
            self.assertNotContains(response, 'other list item 1')
            self.assertNotContains(response, 'other list item 2')

Run unit test, I get expected 404.

    FAIL: test_displays_only_items_for_that_list (lists.tests.ListViewTest)
    AssertionError: 404 != 200 : Couldn't retrieve content: Response code was 404 (expected 200)
    [...]
    FAIL: test_uses_list_template (lists.tests.ListViewTest)
    AssertionError: No templates used to render the response

### Capturing Parameters from URLs

It’s time to learn `how we can pass parameters from URLs to views`:

superlists/urls.py

    urlpatterns = patterns('',
        url(r'^$', 'lists.views.home_page', name='home'),
        url(r'^lists/(.+)/$', 'lists.views.view_list', name='view_list'),
        url(r'^lists/new$', 'lists.views.new_list', name='new_list'),
        # url(r'^admin/', include(admin.site.urls)),
    )

`lists/(.+)/`

`lists/any characters/`

If we go to `/lists/123/`, we get
`view_list(request, "123")`.

But our view doesn’t expect an argument yet! Sure enough, this causes problems:

    ERROR: test_displays_only_items_for_that_list (lists.tests.ListViewTest)
    ERROR: test_uses_list_template (lists.tests.ListViewTest)
    ERROR: test_redirects_after_POST (lists.tests.NewListTest)
    [...]
    TypeError: view_list() takes 1 positional argument but 2 were given

fix it, use a dummy parameter in `views.py`:

lists/views.py

    def view_list(request, list_id):
        [...]

And then we get our expected failure:

    FAIL: test_displays_only_items_for_that_list (lists.tests.ListViewTest)
    AssertionError: 1 != 0 : Response should not contain 'other list item 1'

[To be Modify]

'Let’s make our view discriminate over which items it sends to the template':


lists/views.py

    def view_list(request, list_id):
        list_ = List.objects.get(id=list_id)
        items = Item.objects.filter(list=list_)
        return render(request, 'list.html', {'items': items})

### Adjusting new_list to the New World

Now we get errors in another test:

    ERROR: test_redirects_after_POST (lists.tests.NewListTest)
    ValueError: invalid literal for int() with base 10: 'the-only-list-in-the-world

Source Test.

lists/tests.py

    class NewListTest(TestCase):
        [...]
        def test_redirects_after_POST(self):
            response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
            )
            self.assertRedirects(response, '/lists/the-only-list-in-the-world/')
        
        def test_displays_all_items(self):
            [...]
            response = self.client.get('/lists/the-only-list-in-the-world/'')
            [...]

Change the url.

`'/lists/the-only-list-in-the-world/'` be `'/lists/%d/' % (new_list.id,)`

lists/tests.py

    def test_redirects_after_POST(self):
        response = self.client.post(
        '/lists/new',
        data={'item_text': 'A new list item'}
        )
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

    def test_displays_all_items(self):
        [...]
        response = self.client.get('/lists/%d/' %(list1.id, ))
        [...]

We still get `invalid literal error`.
We change it redirects right url.

lists/views.py

    def new_list(request):
        list_ = List.objects.create()
        Item.objects.create(text=request.POST['item_text'], list=list_)
        return redirect('/lists/%d/' % (list_.id,))

Unit test pass.

Functional test has wrong:

    AssertionError: '2: Use peacock feathers to make a fly' not found in ['1: Use peacock feathers to make a fly']

because we’re now creating a new list for every single POST submission, we have broken the ability to add multiple items to a list. 

>> Notice : if you meet the error in functional test.

>> selenium.common.exceptions.StaleElementReferenceException: Message: stale elemen
t reference: element is not attached to the page document

>> [link](http://stackoverflow.com/questions/32158599/python-selenium-stale-element-exeption)

Todo

- <s>Get FTs to clean up after themselves</s>
- <s>Adjust model so that items are associated with different lists</s>
- <s>Add unique URLs for each list</s>
- <s>Add a URL for creating a new list via POST</s>
- Add URLs for adding a new item to an existing list via POST

## One More View to Handle Adding Items to an Existing List

Todo

- <s>Get FTs to clean up after themselves</s>
- <s>Adjust model so that items are associated with different lists</s>
- <s>Add unique URLs for each list</s>
- <s>Add a URL for creating a new list via POST</s>
- <b>Add URLs for adding a new item to an existing list via POST</b>

We need a URL and view to handle adding a new item to an existing list ( `/lists/<list_id>/
add_item`).

lists/tests.py
    
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

Get

    AssertionError: 0 != 1
    [...]
    AssertionError: 301 != 302 : Response didn't redirect as expected: Response
    code was 301 (expected 302)

### Beware of Greedy Regular Expressions!

Expected the error is `404`.

But you get the `301`. Why?

Because your url pattern is to widthly.

    url(r'^lists/(.+)/$', 'lists.views.view_list', name='view_list'),

When we call the `/lists/1/add_item/`, the patter is match `.+` to `1/add_item`, so has `301`.

`301` is issue a parmanent redirect.

So, Fix it using `\d` to be numerical digits.

    url(r'^lists/(\d+)/$', 'lists.views.view_list', name='view_list'),

Get

    AssertionError: 0 != 1
    [...]
    AssertionError: 404 != 302 : Response didn't redirect as expected: Response
    code was 404 (expected 302)

### The Last New URL

let’s add a new URL for adding new items to existing lists:

superlists/urls.py

    The Last New URLurlpatterns = patterns('',
        url(r'^$', 'lists.views.home_page', name='home'),
        url(r'^lists/(\d+)/$', 'lists.views.view_list', name='view_list'),
        url(r'^lists/(\d+)/add_item$', 'lists.views.add_item', name='add_item'),
        url(r'^lists/new$', 'lists.views.new_list', name='new_list'),
        # url(r'^admin/', include(admin.site.urls)),
    )

Run 

    django.core.exceptions.ViewDoesNotExist: Could not import lists.views.add_item.
    View does not exist in module lists.views.

Todo

- <s>Get FTs to clean up after themselves</s>
- <s>Adjust model so that items are associated with different lists</s>
- <s>Add unique URLs for each list</s>
- <s>Add a URL for creating a new list via POST</s>
- Add URLs for adding a new item to an existing list via POST
- Refactor away some duplication in urls.py

### The Last New View

Todo

- <s>Get FTs to clean up after themselves</s>
- <s>Adjust model so that items are associated with different lists</s>
- <s>Add unique URLs for each list</s>
- <s>Add a URL for creating a new list via POST</s>
- <b>Add URLs for adding a new item to an existing list via POST</b>
- Refactor away some duplication in urls.py

lists/views.py

    def add_item(request):
        pass

Get

    TypeError: add_item() takes 1 positional argument but 2 were given

Then 

lists/views.py

    def add_item(request, list_id):
        pass

And then

    ValueError: The view lists.views.add_item didn't return an HttpResponse object.
    It returned None instead.

lists/views.py

    def add_item(request, list_id):
        list_ = List.objects.get(id=list_id)
        return redirect('/lists/%d/' % (list_.id,))

and then 

    self.assertEqual(Item.objects.count(), 1)
    AssertionError: 0 != 1

save new item

    def add_item(request, list_id):
        list_ = List.objects.get(id=list_id)
        Item.objects.create(text=request.POST['item_text'], list=list_)
        return redirect('/lists/%d/' % (list_.id,))

then 

    Ran 9 tests in 0.050s
    OK

### But How to Use That URL in the Form?

lists/templates/list.html

    <form method="POST" action="but what should we put here?">

Change be

    <form method="POST" action="/lists/{{ list.id }}/add_item">

view will have to pass the list to the template.

Write a new unit test in ListViewTest.

lists/tests.py

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)

`response.context` represents the context we’re going to pass into the render function
—the Django test client puts it on the `response` object for us, to help with testing.

Get

    KeyError: 'list'

Because we’re not passing list into the template.

lists/views.py

    def view_list(request, list_id):
        list_ = List.objects.get(id=list_id)
        return render(request, 'list.html', {'list': list_})

Get

    AssertionError: False is not true : Couldn't find 'itemey 1' in response

fix it in `list.html`

lists/templates/list.html
    
    <form method="POST" action="/lists/{{ list.id }}/add_item">

    [...]

        {% for item in list.item_set.all %}
        <tr><td>{{ forloop.counter }}: {{ item.text }}</td></tr>
        {% endfor %}   

`.item_set` is called a “reverse lookup”—it’s one of Django’s incredibly useful bits of ORM that lets you look up an object’s related items from a different table

Get

    Ran 10 tests in 0.060s
    OK

    $ python manage.py test functional_tests
    Creating test database for alias 'default'...
    .
    ---------------------------------------------------------------------
    Ran 1 test in 5.824s
    OK
    Destroying test database for alias 'default'...

Todo

- <s>Get FTs to clean up after themselves</s>
- <s>Adjust model so that items are associated with different lists</s>
- <s>Add unique URLs for each list</s>
- <s>Add a URL for creating a new list via POST</s>
- <s>Add URLs for adding a new item to an existing list via POST</s>
- Refactor away some duplication in urls.py

## A Final Refactor Using URL includes

Then we replace three lines in superlists/urls.py with an include. Notice that include can take a part of a URL regex as a prefix, which will be applied to all the included URLs (this is the bit where we reduce duplication, as well as giving our code a better structure):

superlists/urls.py

    urlpatterns = patterns('',
        url(r'^$', 'lists.views.home_page', name='home'),
        url(r'^lists/', include('lists.urls')),
        # url(r'^admin/', include(admin.site.urls)),
    )

lists/urls.py

    from django.conf.urls import patterns, url


    urlpatterns = patterns('',
        url(r'^(\d+)/$', 'lists.views.view_list', name='view_list'),
        url(r'^(\d+)/add_item$', 'lists.views.add_item', name='add_item'),
        url(r'^new$', 'lists.views.new_list', name='new_list'),
    )

Todo

- <s>Get FTs to clean up after themselves</s>
- <s>Adjust model so that items are associated with different lists</s>
- <s>Add unique URLs for each list</s>
- <s>Add a URL for creating a new list via POST</s>
- <s>Add URLs for adding a new item to an existing list via POST</s>
- <s><b>Refactor away some duplication in urls.py</b></s>
