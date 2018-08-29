FROM kobayurii/ubn_p3

ADD . /opt/www

WORKDIR /opt/www

RUN pip3 install -r requirements.txt

EXPOSE 8000
