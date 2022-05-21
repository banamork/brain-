FROM python:3.6
 
WORKDIR  /usr/src/.

RUN apt-get update
RUN apt-get install -y gcc make apt-transport-https ca-certificates build-essential 

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR .

COPY . . 

RUN pip install -q deeppavlov==0.4.0
RUN python -m deeppavlov install fasttext_avg_autofaq -d
RUN python -m deeppavlov install fasttext_tfidf_autofaq -d
RUN python -m deeppavlov install tfidf_autofaq -d
RUN python -m deeppavlov install tfidf_logreg_autofaq -d
RUN python -m deeppavlov install tfidf_logreg_en_faq -d
RUN ls -la ./brain.py

CMD ["python3", "./brain.py"]
