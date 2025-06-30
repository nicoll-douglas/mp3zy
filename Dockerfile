FROM python:3.12-slim

# Install ffmpeg and system dependencies
RUN apt-get update \
  && apt-get install -y ffmpeg \
  && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

RUN python3 -m venv .pyvenv
RUN bash -c "source .pyvenv/bin/activate"

# Copy application files
COPY src/ src/
COPY main.py .
COPY setup.py .
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run app
CMD ["python", "main.py"]