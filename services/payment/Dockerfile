# Use the official Ruby image from the Docker Hub
FROM ruby:3.3.0

# Install dependencies
RUN apt-get update -qq && apt-get install -y build-essential libpq-dev

# Set the working directory inside the Docker container
WORKDIR /app

# Copy the Gemfile and Gemfile.lock from your host to your docker container
COPY Gemfile* ./

# Install all the gems
RUN bundle install

# Copy the rest of the application code from your host to your docker container
COPY . .

# Expose port 9292
EXPOSE 9292

# Start the application
CMD ["rackup", "--host", "0.0.0.0"]