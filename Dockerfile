FROM python:3.7.11

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR .

COPY . .

#ENTRYPOINT ["tail", "-f", "/dev/null" ]

ADD bot.py /
CMD [ "python", "./bot.py" ]
