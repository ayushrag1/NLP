FROM python:3.8
# Install system dependencies required by PyTorch
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

COPY ./myapp /app
WORKDIR /app
# Install PyTorch with CPU support
RUN pip install torch==1.13.1+cpu  -f https://download.pytorch.org/whl/torch_stable.html

RUN pip install -r requirements.txt
CMD python app.py