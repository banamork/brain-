FROM python:3.7.11

WORKDIR /usr/src/app
RUN pip install deeppavlov

WORKDIR .

COPY . .

RUN python -m deeppavlov train model.json

#ENTRYPOINT ["tail", "-f", "/dev/null" ]

ADD brain.py /
CMD [ "python", "./brain.py" ]
