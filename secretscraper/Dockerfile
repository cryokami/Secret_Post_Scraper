FROM selenium/standalone-firefox
USER root
RUN apt update -y
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN mkdir /project
COPY requirements.txt /project
WORKDIR /project
RUN pip3 install -r requirements.txt
COPY . /project
RUN chmod 777 geckodriver.log
USER seluser
ENTRYPOINT ["./wait-for-it.sh", "translation:5000", "--timeout=0","--strict","--","python3","webscraper.py"]



