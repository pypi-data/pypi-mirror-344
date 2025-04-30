# Flask-Nestify

Flask-Nestify is a Python library that provides a wrapper around Flask, enabling developers to build REST APIs with a structure and style similar to the Nest.js framework. It simplifies the development process by introducing modularity, decorators, and a clear separation of concerns.

## Features

- **Decorators**: Use decorators to define routes, middleware, and request handlers.
- **Dependency Injection**: Simplify service management with built-in dependency injection.
- **Nest.js-like Structure**: Write Flask applications with a familiar Nest.js-inspired structure.

## Installation

```bash
pip install flask-nestify
```

## Quick Start

Here's an example of how to use Flask-Nestify:


```python
# app.py
from flask import Flask
from flask_nestify import Nestify, Controller, Get

flask_app = Flask(__name__)
app = Nestify(flask_app)

if __name__ == '__main__':
    flask_app.run()
```

```python
# hello_controller.py
from flask_nestify import Controller, Get

class HelloController(Controller):
    @Get('/hello')
    def hello(self):
        return {'message': 'Hello, World!'}
```

## Documentation

For detailed usage and advanced features, please refer to the [documentation](#).

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

Inspired by the [Nest.js](https://nestjs.com/) framework and built with the power of [Flask](https://flask.palletsprojects.com/).