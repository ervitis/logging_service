# Logging service in Python

Use this service to send logs using the HTTPHandler, FileSystemHandler and StreamHandler

If you want, you can try these scripts using __virtualenv__ before you install the libraries

## Status

![[Build Status](https://circleci.com/gh/ervitis/logging_service.png?circle-token=:circle-token)(https://circleci.com/gh/ervitis/logging_service)]

## Try it

First install the libraries needed using __pip__

> pip install -r requirements.txt -U

Then start the server. In this case I am using gunicorn:

> bash start_server.sh

Finally execute the python script:

> python logging_service.py

## Example using it as a library

```python
import logging_service


def main():
    srv_file_logging = logging_service.FileLogging(level=logging_service.ERROR)
    srv_http_logging = logging_service.PostLogging(
        host='127.0.0.1',
        port=8000,
        url_path='/message',
        level=logging_service.DEBUG
    )

    services = [srv_file_logging, srv_http_logging]

    logging_service.Logging.set_services(services).send('Hello world!')


if __name__ == '__main__':
    main()
```

[MIT LICENSE](./LICENSE)