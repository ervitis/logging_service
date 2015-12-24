# Logging service in Python

Use this service to send logs using the HTTPHandler, FileSystemHandler and StreamHandler

If you want, you can try these scripts using __virtualenv__ before you install the libraries

First install the libraries needed using __pip__

> pip install -r requirements.txt -U

Then start the server. In this case I am using gunicorn:

> bash start_server.sh

Finally execute the python script:

> python main.py