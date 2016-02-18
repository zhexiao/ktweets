# ktweets




Table of Contents  
-------------------
[Installation](#Installation)  



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
