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
	│ 	├── admin.py
	│ 	├── __init__.py
	│ 	├── migrations
	│ 	│	 └── __init__.py
	│ 	├── models.py
	│ 	├── tests.py
	│ 	└── views.py
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

用`{{}}`用來拿取Python objects

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

	
	python3 manage.py test functional_tests