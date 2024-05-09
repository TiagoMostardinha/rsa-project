# Define the base image (choose a slim version for efficiency)
FROM python:alpine3.18

# Set the working directory for the container
WORKDIR /app

# Copy your application code to the working directory
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the port your application uses (if applicable)
#EXPOSE 8000

# Specify the command to run your application
ENTRYPOINT [ "python3", "ok.py" ]

