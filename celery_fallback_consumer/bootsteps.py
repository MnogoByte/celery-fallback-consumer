# -*- coding: utf-8 -*-

from __future__ import absolute_import

from celery import bootsteps
from celery.utils.log import worker_logger as logger
from celery.worker import state as worker_state
from celery.platforms import signals as _signals


class FallbackConsumer(bootsteps.StartStopStep):
    conditional = True
    requires = (
        'celery.worker.consumer:Connection',
    )

    def __init__(self, consumer, **kwargs):
        self.enabled = getattr(consumer.app.conf, 'CELERY_FALLBACK_CONSUMER', True)

    def create(self, consumer):
        self.consumer = consumer
        self.stop_worker = consumer.controller.stop
        self.stopped = False

        def stop(*args, **kwargs):
            self.stopped = True
            self.stop_worker(*args, **kwargs)

        consumer.controller.stop = stop

    def stop(self, *args, **kwargs):
        if self.stopped:
            return
        
        for request in worker_state.active_requests:
            if request.task.acks_late and getattr(
                request.task,
                'fallback_terminate',
                getattr(self.consumer.app.conf,
                    'CELERY_FALLBACK_TERMINATE',
                    True
                )
            ):
                request.acknowledged = True
                self.consumer.pool.terminate_job(
                    request.worker_pid, 
                    _signals.signum(
                        getattr(
                            request.task,
                            'fallback_terminate_signal',
                            getattr(self.consumer.app.conf,
                                'CELERY_FALLBACK_TERMINATE_SIGNAL',
                                'SIGTERM'
                            )
                        )
                    )
                )
