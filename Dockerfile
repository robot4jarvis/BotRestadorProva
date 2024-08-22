FROM python:3.12.4-slim AS bot

VOLUME volTelegram
ENV BOTTOKEN=7124346648:AAGHJeUM47ZYhmgiCLu8qEv7pqwn8hrRivc
ADD main.py ./
ADD data.txt ./
RUN pip install python-telegram-bot --upgrade
CMD ["python", "./main.py"]
