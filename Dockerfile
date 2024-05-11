FROM python:3.11

ARG APP_VERSION
ENV APP_VERSION=$APP_VERSION

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY app /app

# Copy entrypoint.sh
COPY entrypoint.sh /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 5000

## Run entrypoint.sh
ENTRYPOINT ["sh", "/app/entrypoint.sh"]