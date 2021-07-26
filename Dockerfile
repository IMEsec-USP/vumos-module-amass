FROM python:3

# TODO: Prepare required image

# Go to app folder
WORKDIR /usr/src/app

# Install required python packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-u", "main.py" ]