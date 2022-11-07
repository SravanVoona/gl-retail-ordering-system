FROM python:3.9
WORKDIR /
RUN apt-get update
RUN apt install -y libgl1-mesa-glx
COPY . .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "run.py" ]
