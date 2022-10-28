FROM python:3.9
WORKDIR /
COPY . .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT [ "bash" ]
CMD [ "shell_run.sh" ]
