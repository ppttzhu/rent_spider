FROM amazonlinux:latest

RUN yum -y update
RUN yum -y install git
RUN yum -y install wget
RUN yum -y install tar
RUN yum -y install bzip2
RUN yum -y install which

# install mysql and gcc for MySQLdb
RUN yum -y install https://dev.mysql.com/get/mysql80-community-release-el7-5.noarch.rpm
RUN yum -y install mysql-community-server
RUN yum -y install mysql-community-devel.x86_64
RUN yum -y install python3-devel
RUN yum -y install gcc
# install firefox browser
RUN wget -O- "https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64&lang=en-US" | tar -jx -C /usr/local/
RUN ln -s /usr/local/firefox/firefox /usr/bin/firefox
# firefox dependencies
RUN yum -y install libXinerama.x86_64 cups-libs dbus-glib alsa-lib libappindicator-gtk3 liberation-fonts
# for headed browser, because headless will be blocked
RUN yum -y install Xvfb

# pull code and install dependency
RUN git clone https://github.com/ppttzhu/rent_spider.git
RUN python3 -m pip install -r rent_spider/requirements.txt
# install firefox driver
RUN python3 -m playwright install firefox
# secret is used for remote database access
COPY secrets.cfg rent_spider/secrets.cfg