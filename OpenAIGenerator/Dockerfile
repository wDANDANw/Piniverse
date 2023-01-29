# Select official python 3 runtime
FROM python:3.6

# Creates a directory in /usr/src/app
RUN mkdir -p /usr/src/app

# Change work directory to it
WORKDIR /usr/src/app

# Copy current directory into the created directory
COPY . /usr/src/app

# Install all dependencies
RUN pip install -r requirements.txt

# Spacy
RUN python3 -m spacy download en_core_web_sm

# Expose the port
EXPOSE 5000

# Start the application
# https://stackoverflow.com/questions/29663459/python-app-does-not-print-anything-when-running-detached-in-docker
CMD ["python", "-u", "main.py"]
