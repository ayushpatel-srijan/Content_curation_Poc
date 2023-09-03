FROM python:3.11-slim-buster

# Install required packages
RUN apt-get update && apt-get install -y openssh-client build-essential && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install NLTK and download the "punkt" resource
RUN pip install nltk
RUN python -m nltk.downloader punkt

# Copy SSH key to the container
COPY chat_gpt_demo.pem /root/.ssh/
RUN chmod 600 /root/.ssh/chat_gpt_demo.pem

# Configure SSH
RUN echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config

# Expose required ports
EXPOSE 8080
EXPOSE 8501

# Set the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy the Streamlit app file
COPY . /app/.

# Set the entrypoint command
ENTRYPOINT ["/entrypoint.sh"]
