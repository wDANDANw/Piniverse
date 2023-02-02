# syntax=docker/dockerfile:1
FROM nvcr.io/nvidia/tensorflow:22.12-tf2-py3

# Install dependencies
RUN apt-get update && apt-get install -y ffmpeg
WORKDIR /install
COPY ./requirements.txt .

RUN pip install -r requirements.txt

# (optional) install nvdiffrast for exporting textured mesh (if use --save_mesh)
RUN pip install git+https://github.com/NVlabs/nvdiffrast/

# (optional) install CLIP guidance for the dreamfield setting
RUN pip install git+https://github.com/openai/CLIP.git

# Creates a directory in /usr/src/app
RUN mkdir -p /usr/src/app

# Change work directory to it
WORKDIR /usr/src/app

# Copy source code
COPY . /usr/src/app

# Start application
# https://stackoverflow.com/questions/29663459/python-app-does-not-print-anything-when-running-detached-in-docker
# CMD ["python", "-u", "main.py", "--text", "'a manburger'", "--workspace", "trial", "-O"]