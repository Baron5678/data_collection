from celery import Celery
# Celery application configuration
# Redis is used as both broker and result backend
app = Celery('data_collection', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

app.conf.broker_transport_options = {'visibility_timeout': 3600,
                                     'retry_policy': { 'timeout': 5.0 }
                                    }
app.conf.result_expires = 10