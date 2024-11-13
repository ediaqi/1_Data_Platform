FROM python:3.11
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 8501
ENTRYPOINT [ "streamlit", "run" ]
CMD ["/app/main.py"]