FROM python:3.11-slim-buster
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 8501
COPY . /app

ENTRYPOINT [ "streamlit", "run" ]
CMD ["main.py"]
