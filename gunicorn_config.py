command = '/usr/local/bin/gunicorn'
pythonpath = '/app'
bind = '0.0.0.0:8000'
workers = 3
# For production, consider using a more robust logging solution like syslog or a dedicated log management service.
# accesslog = '/var/log/gunicorn/access.log'
# errorlog = '/var/log/gunicorn/error.log'
loglevel = 'info'
# For better performance, use a worker class like gevent or eventlet if you have long-running requests or I/O-bound tasks.
# worker_class = 'gevent'
# preload_app = True # For zero-downtime restarts

# Configure the number of threads for each worker.
# This can be beneficial for applications that are I/O bound.
threads = 2
