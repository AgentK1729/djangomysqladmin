This app is written by and belongs to Tejas Sathe

Hi guys!
Like PHP's MySQL Admin, I've built a MySQL admin for Django.
Even though Django ships its own admin interface (which is awesome by the way), I've included some changes that make it more user friendly.
This is still a prototype and I'm yet to add an attractive UI and other database functions.
The awesome thing about this application is that you just paste it in your Django project, configure it a little (which I will explain how)
and you're ready to go!
Here's how to configure:

First, copy the djangoMySQLadmin folder to where your apps are located

In urls.py, add the following line:
url(r'^djangomysqladmin/', include('projectname.djangoMySQLadmin.urls')),

In settings.py, in INSTALLED_APPS, add the following line:
'projectname.djangoMySQLadmin',

In settings.py, in TEMPLATE_DIRS, add the following line:
/path/to/project/djangoMySQLadmin/templates

In settings.py, in TEMPLATE_DIRS, add the following line:
/path/to/project/djangoMySQLadmin/templates

In settings.py, in STATICFILES_DIRS, add the following line:
/path/to/project/djangoMySQLadmin/static

If you're using Django version below 1.6, open urls.py in djangoMySQLadmin, and
change: from django.conf.urls import *
to: from django.conf.urls.defaults import *

In urls.py in djangoMySQLadmin:
change: urlpatterns = patterns ('adbms.djangoMySQLadmin.views',
to: urlpatterns = patterns ('projectname.djangoMySQLadmin.views',
Put the name of your project in place of 'projectname'
