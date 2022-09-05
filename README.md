# Load Generator

Small tool allows to make performance testing, based on swagger specification.
I'm really bad technical writer.)

### Installation
Just clone repository from GitHub.
```bash
git clone git@github.com:abaradulkin/load_generator.git
```
And don't forget to install all required python modules:
```bash
pip install -r requirements.txt
```

### Usage
```bash
usage: main.py [-h] target swagger_json config

positional arguments:
  target        Host URL to be loaded
  swagger_json  Path or URL to swagger file
  config        Path to load config file

optional arguments:
  -h, --help    show this help message and exit
```

Tested on:
+ Wallarm API (https://apiconsole.ru1.wallarm.ru/#/)
+ PetStore API (https://petstore.swagger.io/)