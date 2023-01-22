FROM python:3.9-alpine
WORKDIR /src
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt
COPY ./api /src/api
EXPOSE 8076
CMD [ "uvicorn", "api.godbo:app", "--host", "0.0.0.0", "--port", "8076", "--root-path", "${API_ROOT_PATH-/}" ]
