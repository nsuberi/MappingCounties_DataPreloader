FROM python:3.6
MAINTAINER Nathan Suberi <nsuberi@gmail.com>
ENV NAME ${NAME}

# install core libraries
RUN apt-get update
RUN pip install -U pip

# install application libraries
RUN pip install --upgrade pip && pip install \
    requests \
    census \
    us \
    pandas \
    psycopg2 \
    sqlalchemy

# copy the application folder inside the container
RUN mkdir -p /opt/$NAME/data
WORKDIR /opt/$NAME/
COPY contents/ .
VOLUME /opt/$NAME/data

#RUN groupadd -r $NAME && useradd -r -g $NAME $NAME
#RUN chown -R $NAME:$NAME /opt/$NAME/
#USER $NAME

# Launch script
CMD ["python", "main.py"]
