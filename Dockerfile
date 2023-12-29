FROM ubuntu:22.04

WORKDIR /app

COPY . /app/

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    build-essential \
    python3-pip
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y --fix-missing

RUN curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname -s)-$(uname -m).sh" \
    && bash Miniforge3-$(uname -s)-$(uname -m).sh -b -p /app/env \
    && rm Miniforge3-$(uname -s)-$(uname -m).sh

# Add Miniforge binaries to PATH
ENV PATH=/app/env/bin:$PATH

# Activate the Miniforge environment
SHELL ["/bin/bash", "-c"]
RUN source /app/env/bin/activate

# Install Python 3.10.12
RUN conda install python=3.10.12 -y

# Install motionalbums package in editable mode and its requirements
# Editable mode is currently required to locate packages from the submodules
RUN python -m pip install -e .

# Expose any required ports
EXPOSE 5000

CMD ["uvicorn", "src.facedetectionapp.main:app", "--host", "0.0.0.0", "--port", "5000"]