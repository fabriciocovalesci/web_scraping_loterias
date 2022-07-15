FROM python:3.10.4


RUN apt-get update \
    && apt-get install -y --no-install-recommends libmagic1 locales \
    && rm -rf /var/lib/apt/lists/*
RUN sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && locale-gen

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "./app/main.py"]

CMD [ URL]