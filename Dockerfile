FROM python:3.12.4

ADD main.py ./
ADD data.txt ./
ADD TOKEN.txt ./
RUN pip install python-telegram-bot --upgrade
RUN pip install python-telegram-bot unicodedata datetime
CMD ["python", "./main.py"]
