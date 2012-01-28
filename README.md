## Installation (Debian 6 Squeeze) ##
1. Add to Debian source.list:
`deb http://nginx.org/packages/debian/ squeeze nginx`
`deb-src http://nginx.org/packages/debian/ squeeze nginx`
2. `sudo apt-get update`
3. `sudo apt-get install nginx python-dev python-mysqldb rubygems openjdk-6-jdk icedtea6-plugin mysql-server mysql-client libjpeg62 libjpeg62-dev zlib1g-dev ffmpegthumbnailer xvfb xserver-xephyr iceweasel flashplugin-nonfree`
4. Download http://pypi.python.org/pypi/setuptools
and `sudo python setup.py install`
5. `sudo easy_install django flup selenium pil simplejson python-memcached pyvirtualdisplay postmarkup pygments django-mediagenerator django-tagging django-celery django-ratings django-social-auth django-profiles django-registration django-debug-toolbar`
6. Download https://github.com/thornomad/django-hitcount
and `sudo python setup.py install`
7. `sudo gem install sass compass`