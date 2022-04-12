# Django React Boilerplate

## Setup Step

1. Create React App

	`npx create-react-app django-react-boilerplate`
	
	`cd django-react-boilerplate`
	
	```
	django-react-boilerplate
	├── node_modules
	├── public
	├── src
	├── package.json
	└── package-lock.json
	```
2. Create Django Porject
	
	1. create `requirements.txt`
		```
		django
		gunicorn
		django-heroku
		django-environ
		requests
		whitenoise
		djangorestframework
		```
	
	2. setup virtual environment
	
		`pipenv install -r requirements.txt`
		
		`pipenv shell`
		
	3. create django project
		
		`django-admin startproject backend .`
		
		```
		django-react-boilerplate
		├── backend
		│   ├── __init__.py
		│   ├── asgi.py
		│   ├── settings.py
		│   ├── urls.py
		│   └── wsgi.py
		├── node_modules
		├── public
		├── src
		├── package.json
		├── package-lock.json
		├── manage.py
		├── Pipfile
		├── Pipfile.lock
		└── requirements.txt
		```
		
3. Create App `frontend`
	
	`python manage.py startapp frontend`

4. Update React setting

	1. Move `public` and `src` under `frontend`

    2. Create `package.json` under `frontend`
        ```javascript
        {
        }
        ```
	
	3. Create `static` directory inside `frontend/public` 
		And move files except `index.html` into `static`
		
		```
		frontend
		├── src
		├── public
		│   ├── index.html
		│   └── static
		│  	    ├── favicon.ico
		│  	    ├── logo192.png
		│  	    ├── logo512.png
		│  	    └── manifest.json
		└── package.json
		```

	4. Update `package.json` at the root directory
	
	```javascript
	{
	  "scripts": {
	      ...
	   	  "build": "cd frontend && react-scripts build",
	   	  ...
	  },
	  ...
	  "proxy": "http://localhost:8000"
	}
	```
		
5. Update Django Setup

	1. Update `frontend/views.py`
	
		```python
		from django.views.generic import TemplateView
		from django.views.decorators.cache import never_cache

		# Serve Single Page Application
		indexView = never_cache(TemplateView.as_view(template_name='index.html'))
		```
		
	2. Create `frontend/urls.py`

		```python
		from django.urls import path
		from .views import (
			indexView, 
		)

		app_name = 'frontend'
		urlpatterns = [
			path('', indexView, name='index'),
		]
		```
	
	3. Update `backend/urls.py`
	
		```python
		from django.contrib import admin
		from django.urls import path, include

		urlpatterns = [
			path('', include('frontend.urls')),
			path('admin/', admin.site.urls),
		]
		```
		
	4. update `backend/setttings.py`
		* django_heroku
			```python
			import django_heroku

			django_heroku.settings(locals())
			```

		* rest_framework, custom app
			```python
			INSTALLED_APPS = [
				...
				'rest_framework',
				'frontend',
			]
			```

		* whitenoise
			```python
			MIDDLEWARE = [
				'django.middleware.security.SecurityMiddleware',
				'whitenoise.middleware.WhiteNoiseMiddleware', 
				...
			]

			# Simplified static file serving.
			# https://warehouse.python.org/project/whitenoise/
			STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
			```
		* templates
			```python
			TEMPLATES = [
				{
					...
					'DIRS': [
						os.path.join(BASE_DIR, 'frontend', 'build')
					],
					...
				}
			]
			```

		* static files
			```python
			import os
			
			STATIC_URL = '/static/'
			STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
			STATICFILES_DIRS = [
				os.path.join('frontend', 'build', 'static'),
			]
			```

6. Procfile
	```
	release: python manage.py migrate
	web: gunicorn backend.wsgi
	```
	Procfile.window
	```
	web: python manage.py runserver 0.0.0.0:5000
	```

7. Modularize Django settings
	
	A new folder `settings` under `backend`
	
	Move `settings.py` to `settings/base.py`

	Update `settings/base.py`
	```python
	BASE_DIR = Path(__file__).resolve().parent.parent.parent
	```

	Update `backend/asgi.py`, `backend/wsgi.py`, `manage.py`
	```python
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.base')
	```

8. Add settings for Heroku
	
	Create new file `heroku.py` in `backend/settings`

	```python
	import environ

	# If using in your own project, update the project namespace below
	from backend.settings.base import *

	env = environ.Env(
		# set casting, default value
		DEBUG=(bool, False)
	)

	# False if not in os.environ
	DEBUG = env('DEBUG')

	# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
	SECRET_KEY = env('SECRET_KEY')

	ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

	# Parse database connection url strings like psql://user:pass@127.0.0.1:8458/db
	DATABASES = {
		# read os.environ['DATABASE_URL'] and raises ImproperlyConfigured exception if not found
		'default': env.db(),
	}
	```

9. Directory structure
    ```
    django-react-boilerplate
    ├── backend
    │   ├── settings
    │   │   ├── base.py    // Django develop setting
    │   │   └── heroku.py  // Django Heroku Production setting
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── frontend
    │   ├── build          // React App Build Directory
    │   │   └── static
    │   ├── src            // React App Source Directory
    │   ├── public         // React App Public Directory
    │   │   ├── index.html
    │   │   └── static
    │   ├── package.json
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── manage.py
    ├── package-lock.json
    ├── package.json
    ├── Pipfile
    ├── Pipfile.lock
    ├── Procfile
    ├── Procfile.windows
    └── requirements.txt
    ```
	
10. Build & Run server
	
	`npm run build`
	
	`python manage.py collectstatic`
	
	`python manage.py runserver`

11. Deploy to Heroku

    Create App in Heroku
    ```
    heroku create
    ```

    Setting Environment Variable
    ```
    heroku config:set ALLOWED_HOSTS=<heroku app url>
    heroku config:set DJANGO_SETTINGS_MODULE=backend.settings.heroku
    heroku config:set SECRET_KEY=<secert key>
    ```

    Add Buildpack
    ```
    heroku buildpacks:add --index 1 heroku/nodejs
    heroku buildpacks:add --index 2 heroku/python
    ```

    Add Postgres Add-on
    ```
    heroku addons:create heroku-postgresql:hobby-dev
    ```
    
### Setup after clone from Github

1. re-install node_modules

```
npm i
```

2. Re-create virtual environment

```
pipenv install -r requirements.txt	
```

### Reference:

<https://dev.to/shakib609/deploy-your-django-react-js-app-to-heroku-2bck>

<https://blog.heroku.com/from-project-to-productionized-python>
