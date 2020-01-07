FROM raspbian/stretch

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install python3 -y
RUN pwd
RUN whoami

ADD src/client /client
RUN ls /client
RUN python3 --version
