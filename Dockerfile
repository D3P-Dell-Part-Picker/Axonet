FROM raspbian/stretch

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install python3 -y
RUN apt-get install binutils build-essential cpp cpp-6 dbus dpkg-dev fakeroot g++ g++-6 gcc gcc-6 gir1.2-glib-2.0 libalgorithm-diff-perl libalgorithm-diff-xs-perl libalgorithm-merge-perl libasan3 libatomic1 libc-dev-bin libc6-dev libcc1-0 libdbus-glib-1-2 libdpkg-perl libexpat1-dev libfakeroot libfile-fcntllock-perl libgcc-6-dev libgdbm3 libgirepository-1.0-1 libglib2.0-0 libglib2.0-data libgomp1 libicu57 libisl15 libmpc3 libmpfr4 libperl5.24 libpython3-dev libpython3.5 libpython3.5-dev libstdc++-6-dev libubsan0 libxml2 linux-libc-dev make manpages manpages-dev netbase patch perl perl-modules-5.24 -y
RUN apt-get install python3-pip -y
ADD docker/requirements.txt .
RUN apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev
RUN pip3 install -r requirements.txt
ADD docker/pyinstall .
RUN ./pyinstall
RUN apt install -y libxml2-dev libxslt-dev python-dev
RUN pip3.6 install python_secrets
RUN pwd
RUN whoami

ADD docker/launchscript.sh .

ADD src /client

ENTRYPOINT ["sh", "./launchscript.sh"]
