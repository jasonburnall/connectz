FROM python:3.6.5-jessie

# Put the code here
WORKDIR /usr/src/app

# Requirements when needed
#COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt

# Keep container alive
CMD tail -f /dev/null