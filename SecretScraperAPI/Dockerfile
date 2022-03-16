FROM python:3.9.7
COPY . ./ScraperAPI
WORKDIR ./ScraperAPI
RUN pip3 install -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["python3","main.py"]