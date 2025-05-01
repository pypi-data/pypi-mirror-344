hathaway_analytics
==================

`hathaway_analytics` is a minimal, non-blocking data analytics system designed for Flask apps. It collects metadata from each incoming request and forwards it to a centralized analytics server for logging and real-time processing.

Features
--------

- Non-blocking data transmission via threading
- Compatible with Flask and Flask-SQLAlchemy
- Supports WebSocket broadcasting of incoming logs
- Configurable endpoint and authentication via .cfg file
- Designed for simple integration across multiple microservices

Installation
------------

To install the package:

    pip install hathaway_analytics

Or install from a local build:

    pip install ./dist/hathaway_analytics-0.1.0-py3-none-any.whl

Usage
-----

In your Flask app:

    from hathaway_analytics import send_data_analytics

    @app.before_request
    def log_request():
        send_data_analytics()

At your centralized analytics server:

    from hathaway_analytics import receive_data_analytics

    @app.route('/log', methods=['POST'])
    def log():
        return receive_data_analytics()

Configuration
-------------

Place a `hathaway_analytics.cfg` file alongside your application with contents like:

    [analytics]
    endpoint = https://analytics.hathaway.llc/log
    secret = your-secret-token
    allowed_ips = 192.0.2.1, 198.51.100.42

Identical config files should be placed alongside both your flask app and your centralized server.
Your secret will not be checked if it is left blank and your allowed_ips will not be checked if they are left blank.
In other words, to disable a verification method simply leave it blank in the config file.

License
-------

GPL v3. See the LICENSE file for details.
