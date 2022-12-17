# This is the first stage, it is named requirements-stage.
FROM python:3.10.9 as requirements-stage

# Set /tmp as the current working directory.
# Here's where we will generate the file requirements.txt
WORKDIR /tmp

# Install Poetry in this Docker stage.
RUN pip install poetry

# Copy the pyproject.toml and poetry.lock files to the /tmp directory.
# Because it uses ./poetry.lock* (ending with a *), it won't crash if that file is not available yet.
COPY ./pyproject.toml ./poetry.lock* /tmp/

# Generate the requirements.txt file.
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# This is the final stage, anything here will be preserved in the final container image.
FROM python:3.10.9

# Set the current working directory to /code.
WORKDIR /code

# Copy the requirements.txt file to the /code directory.
# This file only lives in the previous Docker stage, that's why we use --from-requirements-stage to copy it.
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

# Install the package dependencies in the generated requirements.txt file.
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the app directory to the /code directory.
COPY ./api /code/api

# Run the uvicorn command, telling it to use the app object imported from app.main.
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
