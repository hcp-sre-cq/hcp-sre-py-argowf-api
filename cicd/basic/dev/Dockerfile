FROM docker-repo.skhynix.com/tiangolo/uvicorn-gunicorn-fastapi:python3.7

# env directory
ENV USER_DIR=/root
ENV WORK_DIR=/app

WORKDIR $USER_DIR
RUN mkdir $USER_DIR/.kube

# file copy
COPY ./pip.conf $USER_DIR/.pip/pip.conf
COPY ./ $WORK_DIR/

# working directory
WORKDIR $WORK_DIR

# pip 설치
RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt

# source code copy
COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
