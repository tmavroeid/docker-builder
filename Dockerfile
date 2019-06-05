FROM alpine:3.8

RUN apk add --no-cache --update\
        python3\
        wget\
	curl

RUN wget -O get-pip.py 'https://bootstrap.pypa.io/get-pip.py'

RUN python3 get-pip.py

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN mkdir /src

WORKDIR /src

COPY simpleapp-tornado.py .

HEALTHCHECK --interval=20s --timeout=10s CMD curl -f http://127.0.0.1:8000/ || exit 1

EXPOSE  8000

CMD ["python3", "simpleapp-tornado.py", "-port=8000"]
