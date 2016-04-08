# kweets

This is description of kweets


## Table of Contents  
- [Requirements](#Requirements)  
- [Installation](#Installation)  
- [Application Config](#Application_Config)  
- [Usage](#Usage)  


<a name="Requirements"/>
## Requirements
- Django 1.9.*
- Django Rest Framework
- Mysql && Redis
- Gevent
- Twitter API


## Installation
<a name="Installation"/>
- VirtualEnv
```shell
    $ virtualenv -p python3 env
```

- Django and Django Rest Framework
```shell
    $ pip install django
    $ django-admin startproject kweets

    $ pip install djangorestframework
    $ pip install markdown       # Markdown support for the browsable API.
    $ pip install django-filter  # Filtering support
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



<a name="Application_Config"/>
## Application Config
- Upstart config
```shell
    $ sudo vim /etc/init/kweets.conf

    description "uWSGI instance to serve kweets"
    
    start on runlevel [2345]
    stop on runlevel [!2345]
    
    setuid vagrant
    setgid www-data
    
    script
        uwsgi --ini /vagrant/kweets/kweets.ini
    end script
    
    # start the service
    $ sudo start kweets

    # restart the service
    $ sudo restart kweets    
```

- Uwsgi config
```shell
    [uwsgi]
    chdir = /vagrant/kweets
    home = /vagrant/kweets/env
    module = kweets.wsgi:application

    uid = vagrant
    gid = www-data

    master = true
    processes = 5

    socket = /tmp/kweets.sock
    chmod-socket = 664
    vacuum = true  
```

- Nginx config
```shell
    server {
        listen 82;
        server_name 127.0.0.1;

        location = /favicon.ico { access_log off; log_not_found off; }

        location / {
            include uwsgi_params;
            uwsgi_pass unix:/tmp/kweets.sock;
        }
    }
```


## Usage
<a name="Usage"/>
- Running Web Server
```shell
    $ sudo start kweets
    $ sudo service nginx start
```

- Running Twitter Streaming API
```shell
    $ python tweets/scripts/tw_streaming.py 
```
