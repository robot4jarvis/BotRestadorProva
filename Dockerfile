FROM python:3.12.4-slim AS bot

VOLUME volTelegram
ENV BOTTOKEN=${BOTTOKEN}
ADD main.py ./
ADD methods.py ./
ADD data.txt ./
ADD cumples.txt ./
RUN pip install python-telegram-bot[job-queue] --upgrade
CMD ["python", "./main.py"]
