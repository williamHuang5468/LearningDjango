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
            self.assertIn('Hello', self.browser.title)
            #assert 'Hello' in browser.title, "Browser title was " + browser.title
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