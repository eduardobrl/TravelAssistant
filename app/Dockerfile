FROM public.ecr.aws/lambda/python:3.12-x86_64

RUN dnf -y install gcc

COPY requirements.txt ./

RUN python3.12 -m pip install --upgrade -r requirements.txt -t .

COPY . .

RUN rm /var/task/pathlib.py | true

# Command can be overwritten by providing a different command in the template directly.
CMD ["telegram_app.lambda_handler"]
