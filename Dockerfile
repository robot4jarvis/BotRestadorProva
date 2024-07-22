FROM python:3.12.4-slim AS bot

ADD main.py ./
ADD data.txt ./
ADD TOKEN.txt ./
RUN pip install python-telegram-bot --upgrade
CMD ["python", "./main.py"]
