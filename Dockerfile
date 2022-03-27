FROM python:3.9

WORKDIR /fast_api

COPY ./requirements.txt /fast_api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /fast_api/requirements.txt

COPY medium/ /fast_api/medium/

CMD ["uvicorn", "medium.main:app"]
