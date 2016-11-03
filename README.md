# celery-fallback-consumer

[Celery](http://celeryproject.org) consumer blueprint preventing multiple unacked task execution by termination on broker connection errors.

# Problem

Using `RabbitMQ` as broker and `CELERY_ACKS_LATE` option enabled
results multiple task execution in case of broker connection lost or broken.
This module provides workaround terminating active unacked tasks in case of connection problems.
You can specify which kind of tasks you would like to terminate (see **settings** section below).

# Installation & Setup

```#bash
pip install celery-fallback-consumer
pip install git+https://github.com/MnogoByte/celery-fallback-consumer.git
```

Append your `proj/celery.py` file containg `app` instance with the following lines.

```python
import celery_fallback_consumer
celery_fallback_consumer.register(app)
```

# Settings

| Setting | Task attribute | Default | Description |
| ------- | -------------- | ------- | ----------- |
| CELERY_FALLBACK_CONSUMER | N/A | True | Enables fallback consumer if it is registered |
| CELERY_FALLBACK_TERMINATE | fallback_terminate | True | Controls terminating unacked task |
| CELERY_FALLBACK_TERMINATE_SIGNAL | fallback_terminate_signal | `SIGTERM` | Specifies signal sent for termination |

# Author

[Antonov Mikhail](https://github.com/atin65536)

# License

BSD - 3
