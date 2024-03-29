# base image
FROM python:3.9

# application folder
WORKDIR /usr/src/app

# copy req.txt to the application folder
COPY requirements.txt .

# Install python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files to application folder in the base image
COPY . ./

# execute app.py
CMD [ "python", "./app.py" ]