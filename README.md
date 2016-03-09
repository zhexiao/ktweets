# kweets

This is description of kweets


## Table of Contents  
- [Installation](#Installation)  
- [Usage](#Usage)  



## Installation
<a name="Installation"/>
- VirtualEnv
```shell
    $ virtualenv -p python3 env
```

- Django 1.9.2
```shell
    $ pip install django
    $ django-admin startproject kweets
```

- Mysql && redis
```shell
    $ sudo apt-get install python3-dev libmysqlclient-dev
    $ sudo apt-get install redis-server
    $ pip install mysqlclient
    $ pip install redis
```

- Gevent
```shell
    $ pip install wheel
    $ pip install setuptools 'cython>=0.23.4' git+git://github.com/gevent/gevent.git#egg=gevent
```

- Twitter API
```shell
    $ pip install TwitterAPI
```

- Django Rest Framework
```shell
    $ pip install djangorestframework
    $ pip install markdown       # Markdown support for the browsable API.
    $ pip install django-filter  # Filtering support
```



## Usage
<a name="Usage"/>
- Running Web Server
```shell
    $ python manage.py runserver
```

- Running Twitter Streaming API
```shell
    $ python tweets/scripts/tw_streaming.py 
```
