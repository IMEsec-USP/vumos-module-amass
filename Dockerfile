FROM python:3

# Install Amass
RUN wget https://github.com/OWASP/Amass/releases/download/v3.13.4/amass_linux_amd64.zip
RUN unzip amass_linux_amd64.zip
RUN rm amass_linux_amd64.zip

ENV PATH="/amass_linux_amd64:${PATH}"

# Go to app folder
WORKDIR /usr/src/app

# Install required python packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-u", "main.py" ]