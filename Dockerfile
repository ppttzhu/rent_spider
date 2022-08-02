FROM amazonlinux:latest

RUN yum -y update
RUN yum -y install git
RUN yum -y install wget
RUN yum -y install tar
RUN yum -y install bzip2

# install mysql and gcc for MySQLdb
RUN yum -y install https://dev.mysql.com/get/mysql80-community-release-el7-5.noarch.rpm
RUN yum -y install mysql-community-server
RUN yum -y install mysql-community-devel.x86_64
RUN yum -y install python3-devel
RUN yum -y install gcc
# install chrome for selenium
RUN yum -y install https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
RUN wget -O- "https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64&lang=en-US" | tar -jx -C /usr/local/
RUN ln -s /usr/local/firefox/firefox /usr/bin/firefox
RUN yum -y install libXinerama.x86_64 cups-libs dbus-glib
# for headed browser
RUN yum -y install Xvfb