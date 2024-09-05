FROM python:3.11.9-slim


WORKDIR /app

COPY ../app/requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY /app /app


EXPOSE 8082

RUN cd /app

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8082"]
