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