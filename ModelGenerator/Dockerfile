# Select official python 3 runtime
FROM python:3.7

# Creates a directory in /usr/src/app
RUN mkdir -p /usr/src/app/ModelGenerator

# Change work directory to it
WORKDIR /usr/src/app/ModelGenerator

# Copy current directory into the created directory
COPY . /usr/src/app/ModelGenerator

# Install all dependencies
RUN pip install -e ./candidates/openai_point_e/

# Install Requirements
Run pip install -r requirements.txt

# Expose the port
EXPOSE 5000

# Start the application
# https://stackoverflow.com/questions/29663459/python-app-does-not-print-anything-when-running-detached-in-docker
CMD ["python", "-u", "server.py"]

## For debug
#ENTRYPOINT ["tail", "-f", "/dev/null"]