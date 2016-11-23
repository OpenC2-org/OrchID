
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.python.org/pypi/hug/)

# OrchID - Orchestrator for Intelligent Defence

***

OrchID is an OpenC2 proxy built in Django 1.10.2. OrchID aims to provide a simple, modular API to begin accepting OpenC2 commands and converting them into Python actions.

## Setup
---
In it's current state it is a fairly light-weight Django app with few dependencies,

```sh
pip install requests
pip install django==1.10.2
pip install jsonschema
```
OrchID does not currently use a database backend, however later revisions will use one for storing user credentials when I add authentication, so it's best to set one up now. The project comes shipped with the settings necessary for setting up MySQL, but any Django database engine should work fine, you will just need to create a database called "orchid" and a user to connect to it.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'orchid',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}
```

For future reference you may also need to run the following when I get started adding the database functions:

```python
python manage.py makemigrations
python manage.py migrate
```

## Get Started
---
OrchID runs with the standard runserver command:

```python
python manage.py runserver 0.0.0.0:8000
```

This project is a fully-fledged deployment, but the "orchid" folder should stand alone as an importable django app if you want to use it in your project.

Once running, an OpenC2 POST endpoint will be available on `http://<your_ip>/openc2/`. A sample collection of working JSON objects to test sending to the server can be found in ./orchid/samples. 

When the server initialises it loads all profiles specified in the "OPENC2_PROFILES" Django setting, each profile contains a subroutines for handling OpenC2 actions. These routines register which OpenC2 messages they can handle with the use of the @openc2_action decorator. Example profiles for process-dns-service, network-firewall and a notification profile have been included. Custom specifiers must be handled within the subroutine (see the example_process_firewall_juniper.py for an example of this).

## Custom Config
---
OrchID uses the Django settings fill to get information about the actuators it can connect to, currently there are these two:

### OPENC2 Controlled BIND DNS Servers
```python
OPENC2_BIND_DNS_SERVERS = [
    {
                    'hostname':'dns_server_1',
                    'ip':'10.10.10.1',
                    'username':'bind_user',
                    'password':'bind_password',
    },
    {
                    'hostname':'dns_server_2',
                    'ip':'10.10.10.2',
                    'username':'bind_user',
                    'password':'bind_password',
    }
]
```

### OPENC2 Controlled Juniper Firewalls
```python
OPENC2_JUNIPER_FIREWALLS = [
    {
                    'hostname':'r1_juniper',
                    'ip':'10.10.10.1',
                    'version':'SSG5',
                    'public_interfaces':[
                            {"fe-0/0/0":"0.0.0.0/0"},
                        ],
                    'internal_interfaces':[
                            {"fe-0/1/0":"192.168.1.0/24"}
                    ],
                    'username':'juniper_user',
                    'password':'juniper_password',
    },
    {
                    'hostname':'r2_juniper',
                    'ip':'10.10.10.2',
                    'version':'SRX',
                    'public_interfaces':[
                            {"fe-0/0/0":"0.0.0.0/0"},
                        ],
                    'internal_interfaces':[
                            {"fe-0/1/0":"192.168.1.0/24"}
                    ],
                    'username':'juniper_user',
                    'password':'juniper_password',
    }
]
```

These are just to showcase how I envision it working, as no actuator logic is implemented to perform actions on vendor appliances (profiles just print to the console log currently). You can leave these in until you are confident enough to start writing your own profiles.

## Testing
---

I have added two unit tests; they check that JSON samples in the `./sample` folder are syntactically valid, then pass them through the command dispatcher. The tests fail if the dispatcher doesn't return a `200` _(OK)_ status code. Tests can be run with:

```python
python manage.py test orchid
```

## Thanks

---

Large portions of this project are based on the [Yuuki] project by Joshua Brulé. Without Yuuki this project would not exist, as Josh solved some of the fundamental design problems in making OpenC2 proxies a reality. Thanks for kicking down the door for us all Josh.

Also a big thanks to everyone in the OpenC2 community, on conference calls and on Slack, you have always been helpful when I have struggled with understanding components of OpenC2 and I look forward to shaping the future of defence with you all.

[Yuuki]: <https://github.com/OpenC2-org/openc2-yuuki>





