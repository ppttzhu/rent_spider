# app install

sudo yum update
sudo yum install git
sudo yum install tmux

# install mysql and gcc for MySQLdb
sudo yum install https://dev.mysql.com/get/mysql80-community-release-el7-5.noarch.rpm
sudo yum install mysql-community-server
sudo yum install mysql-community-devel.x86_64
sudo yum install python3-devel
sudo yum install gcc
# install chrome for selenium
sudo yum install https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
# install firefox for playwright
wget -O- "https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64&lang=en-US" | sudo tar -jx -C /usr/local/
sudo ln -s /usr/local/firefox/firefox /usr/bin/firefox
sudo yum install libXinerama.x86_64 cups-libs dbus-glib
# for headed browser
sudo yum install Xvfb

# generate ssh and pull code

ssh-keygen
cat ~/.ssh/id_rsa.pub # Then upload to bitbucket
git clone git@bitbucket.org:yixinpeng/rent_spider.git
cd rent_spider

# pip install

python3 -m pip install -r requirements.txt
python3 -m playwright install firefox

# send credential to ec2
scp -i ~/.ssh/macbook-air.pem ./secrets.cfg ec2-user@ec2-3-85-103-227.compute-1.amazonaws.com:/home/ec2-user/rent_spider/secrets.cfg

# Run in remote prod mode
tmux
cd rent_spider
git pull
xvfb-run -- python3 main.py -r

# Run in remote mode with verbose, set
export DEBUG=pw:api