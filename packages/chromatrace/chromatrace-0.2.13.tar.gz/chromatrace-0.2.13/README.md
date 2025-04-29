# Chromatrace
---
[![GitHub](https://img.shields.io/github/license/Msameim181/Python-Logging-Best-Practice.svg)]()
[![Version](https://badge.fury.io/gh/Msameim181%2FPython-Logging-Best-Practice.svg)](https://badge.fury.io/gh/Msameim181%2FPython-Logging-Best-Practice)
[![GitHub Release](https://img.shields.io/github/release/Msameim181/Python-Logging-Best-Practice.svg?style=flat)]()  
[![GitHub Release Date](https://img.shields.io/github/release-date/Msameim181/Python-Logging-Best-Practice.svg?style=flat)]()
[![GitHub Release Date](https://img.shields.io/github/last-commit/Msameim181/Python-Logging-Best-Practice.svg?style=flat)]()  
[![GitHub issues](https://img.shields.io/github/issues/Msameim181/Python-Logging-Best-Practice.svg)]()

[![PyPi Version](https://img.shields.io/pypi/v/chromatrace.svg)](https://pypi.python.org/pypi/chromatrace/)
[![PyPi Version Alt](https://badge.fury.io/py/chromatrace.svg)](https://pypi.python.org/pypi/chromatrace/)  
[![PyPI Downloads](https://static.pepy.tech/badge/chromatrace)](https://pepy.tech/projects/chromatrace)
[![Python Versions](https://img.shields.io/pypi/pyversions/chromatrace.svg)]()


Chromatrace is a Python package designed for advanced logging capabilities, including trace and request ID management along with process ID. It provides a flexible logging configuration and supports colored logging for better visibility.

I believe that logging is an essential part of any application, and it is crucial to have a well-organized and structured logging system. Chromatrace aims to provide a simple and easy-to-use logging system that can be integrated into any Python application.
In simple terms, Chromatrace is a Best Practice of Logging in Python.

## Features

- Configurable logging settings using Pydantic.
- Customizable log levels and loggers for different services.
- Support for trace IDs and request IDs.
- Support for process IDs.
- Customizable log formats and handlers.
- Asynchronous and synchronous function tracing.
- Uvicorn integration for logging configuration to customize log settings.
- FastAPI integration for request ID management.
- SocketIO integration for request ID management.
- Practical examples for different frameworks and use cases.

## Installation

You can install Chromatrace via pip:

```bash
pip install chromatrace
```

## Usage

To use Chromatrace in your application, you can import the necessary components:

```python
from chromatrace import LoggingSettings, LoggingConfig, tracer
```

Configure your logging settings:

```python
logging_config = LoggingConfig(
    settings=LoggingSettings(
        application_level="Development",
        enable_tracing=True,
        ignore_nan_trace=False,
        enable_file_logging=True,
    )
)
logger = logging_config.get_logger(__name__)
```

Use the `tracer` decorator to trace your functions:

```python
@tracer
async def my_async_function():
   logger.debug("Check something")
   logger.info("Doing something")
   logger.warning("Doing something")
   logger.error("Something went wrong")
```

### Dependency Injection using Lagom

```python
from lagom import Container

container = Container()

from chromatrace import LoggingConfig, LoggingSettings

container[LoggingSettings] = LoggingSettings(
        application_level="Development",
        enable_tracing=True,
        ignore_nan_trace=False,
        enable_file_logging=True,
    )
container[LoggingConfig] = LoggingConfig(container[LoggingSettings])
```

Then, add the `LoggingConfig` to your service:

```python
import logging

from chromatrace import LoggingConfig


class SomeService:
    def __init__(self, logging_config: LoggingConfig):
        self.logger = logging_config.get_logger(self.__class__.__name__)
        self.logger.setLevel(logging.ERROR)
    
    async def do_something(self):
        self.logger.debug("Check something in second service")
        self.logger.info("Doing something in second service")
        self.logger.error("Something went wrong in second service")
```

Results:
```log
[Development]-(2024-11-21 23:43:26)-[INFO]-[APIService]-FILENAME:api_app.py-FUNC:do_something-THREAD:MainThread-LINE:27 :: 
Doing something in API service

[Development]-(2024-11-21 23:43:26)-[ERROR]-[APIService]-FILENAME:api_app.py-FUNC:do_something-THREAD:MainThread-LINE:28 :: 
Something went wrong in API service

[T-dc1be4de]-[Development]-(2024-11-21 23:43:26)-[INFO]-[Main]-FILENAME:main.py-FUNC:main-THREAD:MainThread-LINE:21 :: 
Starting main

[T-dc1be4de]-[Development]-(2024-11-21 23:43:26)-[ERROR]-[ExampleService]-FILENAME:example_service.py-FUNC:do_something-THREAD:MainThread-LINE:26 :: 
Something went wrong

[T-dc1be4de]-[Development]-(2024-11-21 23:43:26)-[INFO]-[InnerService]-FILENAME:example_service.py-FUNC:do_something-THREAD:MainThread-LINE:13 :: 
Doing something in second service

[T-dc1be4de]-[Development]-(2024-11-21 23:43:26)-[ERROR]-[InnerService]-FILENAME:example_service.py-FUNC:do_something-THREAD:MainThread-LINE:14 :: 
Something went wrong in second service

[T-dc1be4de]-[Development]-(2024-11-21 23:43:26)-[DEBUG]-[AnotherSample]-FILENAME:sample.py-FUNC:do_something-THREAD:MainThread-LINE:12 :: 
Check something

[T-dc1be4de]-[Development]-(2024-11-21 23:43:26)-[INFO]-[AnotherSample]-FILENAME:sample.py-FUNC:do_something-THREAD:MainThread-LINE:13 :: 
Doing something

[T-dc1be4de]-[Development]-(2024-11-21 23:43:26)-[WARNING]-[AnotherSample]-FILENAME:sample.py-FUNC:do_something-THREAD:MainThread-LINE:14 :: 
Doing something

[T-dc1be4de]-[Development]-(2024-11-21 23:43:26)-[ERROR]-[AnotherSample]-FILENAME:sample.py-FUNC:do_something-THREAD:MainThread-LINE:15 :: 
Something went wrong
```

The two first log was out of trace and the trace ID was not added to the log message. The rest of the logs were within the trace and the trace ID - `T-dc1be4de`, was added to the log message.

**NOTE**: The important thing is that each Class or Service can have its own log level. This is useful when you want to have different log levels for different services.

### FastAPI Integration

```python
from chromatrace.fastapi import RequestIdMiddleware as FastAPIRequestIdMiddleware
from chromatrace.django import RequestIdMiddleware as DjangoRequestIdMiddleware

app = FastAPI()
app.add_middleware(FastAPIRequestIdMiddleware)
```

Result:
```log
[R-ffe0a9a2]-[Development]-(2024-11-22 00:13:53)-[INFO]-[APIService]-FILENAME:api_app.py-FUNC:read_root-THREAD:MainThread-LINE:38 :: 
Hello World

[R-ffe0a9a2]-[Development]-(2024-11-22 00:13:53)-[ERROR]-[ExampleService]-FILENAME:example_service.py-FUNC:do_something-THREAD:MainThread-LINE:26 :: 
Something went wrong

[R-ffe0a9a2]-[Development]-(2024-11-22 00:13:53)-[INFO]-[InnerService]-FILENAME:example_service.py-FUNC:do_something-THREAD:MainThread-LINE:13 :: 
Doing something in second service

[R-ffe0a9a2]-[Development]-(2024-11-22 00:13:53)-[ERROR]-[InnerService]-FILENAME:example_service.py-FUNC:do_something-THREAD:MainThread-LINE:14 :: 
Something went wrong in second service
```

As you can see, the request ID - `R-ffe0a9a2` is automatically added to the log messages from the thread that handles the request.


### SocketIO Integration

```python
from chromatrace.socketio import SocketRequestIdMiddleware

socket_application = SocketRequestIdMiddleware(socket_application)
```
The full example can be found in the [socket_app.py](src/examples/frameworks/socket_app.py) file. I recommend you to check it out before making any decision. The client-side code can be found in the [socket_client.py](src/examples/adaptors/socket_client.py) file.

Result:
```log
[S-4e2b7c5e]-[Development]-(2024-12-06 01:15:18)-[INFO]-[Socket]-FILENAME:socket_app.py-FUNC:connect-THREAD:MainThread-LINE:86 :: 
Socket connected on main namespace. SID: wB-srwnv9Xa2w_8bAAAB

[S-4e2b7c5e]-[Development]-(2024-12-06 01:15:20)-[INFO]-[Socket]-FILENAME:socket_app.py-FUNC:message-THREAD:MainThread-LINE:90 :: 
Received message on main namespace. SID: wB-srwnv9Xa2w_8bAAAB, Message: Hello from the client

[S-aaf46528]-[Development]-(2024-12-06 01:15:47)-[INFO]-[Socket]-FILENAME:socket_app.py-FUNC:connect-THREAD:MainThread-LINE:86 :: 
Socket connected on main namespace. SID: FI3E_S_A-KsTi4RLAAAD

[S-aaf46528]-[Development]-(2024-12-06 01:15:49)-[INFO]-[Socket]-FILENAME:socket_app.py-FUNC:message-THREAD:MainThread-LINE:90 :: 
Received message on main namespace. SID: FI3E_S_A-KsTi4RLAAAD, Message: Hello from the client
```

Yes, the socket logs are also within the trace. The trace ID - `S-4e2b7c5e` and `S-aaf46528` was added to the log messages. For better experience, the prefix `S` was added to the trace ID to differentiate it from the request ID.


### Uvicorn Integration

```python
from chromatrace.uvicorn import GetLoggingConfig, UvicornLoggingSettings

rest_application = FastAPI()

uvicorn.run(
    rest_application,
    host="0.0.0.0",
    port=8000,
    log_level="debug",
    log_config=GetLoggingConfig(
        UvicornLoggingSettings(
            enable_file_logging=True,
            show_process_id=True,
        )
    ),
)
```

Result:
```log
(2024-12-12 20:54:54)-[PID:3710345]-[INFO]: Started server process [3710345]
(2024-12-12 20:54:54)-[PID:3710345]-[INFO]: Waiting for application startup.
(2024-12-12 20:54:54)-[PID:3710345]-[INFO]: Application startup complete.
(2024-12-12 20:54:54)-[PID:3710345]-[INFO]: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
(2024-12-12 20:54:57)-[PID:3710345]-[INFO]: ADDRESS:(127.0.0.1:46166) - REQUEST:"GET /consume HTTP/1.1" - STATUS:200 OK
(2024-12-12 20:55:45)-[PID:3710345]-[INFO]: ADDRESS:(127.0.0.1:54018) - REQUEST:"GET /consume HTTP/1.1" - STATUS:200 OK
(2024-12-12 20:56:51)-[PID:3710345]-[INFO]: ADDRESS:(127.0.0.1:58240) - REQUEST:"GET / HTTP/1.1" - STATUS:200 OK
(2024-12-12 20:56:51)-[PID:3710345]-[INFO]: ADDRESS:(127.0.0.1:58254) - REQUEST:"GET / HTTP/1.1" - STATUS:200 OK
(2024-12-12 20:56:52)-[PID:3710345]-[INFO]: ADDRESS:(127.0.0.1:58260) - REQUEST:"GET / HTTP/1.1" - STATUS:200 OK
(2024-12-12 20:56:52)-[PID:3710345]-[INFO]: ADDRESS:(127.0.0.1:58270) - REQUEST:"GET / HTTP/1.1" - STATUS:200 OK
(2024-12-12 21:16:45)-[PID:3710345]-[INFO]: Shutting down
(2024-12-12 21:16:45)-[PID:3710345]-[INFO]: Waiting for application shutdown.
(2024-12-12 21:16:45)-[PID:3710345]-[INFO]: Application shutdown complete.
(2024-12-12 21:16:45)-[PID:3710345]-[INFO]: Finished server process [3710345]
```

The logs are within the process ID - `PID:3710345` was added to the log messages. The log messages are also colored for better visibility. The log messages are also written to the file if the `enable_file_logging` is set to `True`. For more information, check the [config.py](src/chromatrace/uvicorn/config.py) file, `UvicornLoggingSettings` class.


## Examples

> You don't trust me, do you? I understand. You wanna see it in action, right? I got you covered. :)

You can find examples of how to use Chromatrace in the [examples](src/examples/) directory. Run the examples using the following command:

```bash
python main.py
```

Then, run:
    
```bash
curl 0.0.0.0:8000
```

Now, check the logs in the terminal.

Also, the socket server will start and wait for the client to connect on `http://localhost:8001`.
For socket client-side run the following command in another terminal:

```bash
python adaptors/socket_client.py
```

Now, check the logs in the both terminal.

## License

This project is licensed under the GNU AFFERO GENERAL PUBLIC LICENSE - see the [LICENSE](LICENSE) file for details.

## Ideas and Sources

- [Python Logging Best Practices Tips](https://coralogix.com/blog/python-logging-best-practices-tips/)
- [12 Python Logging Best Practices To Debug Apps Faster](https://middleware.io/blog/python-logging-best-practices/)
- [10 Best Practices for Logging in Python](https://betterstack.com/community/guides/logging/python/python-logging-best-practices/)
