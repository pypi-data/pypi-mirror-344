Ranch
=====

Standardized tooling, monitoring, and retry logic for use with Celery. fork of https://github.com/managedbyq/mbq.ranch

## Installation

Ranch is a Django application. To use Ranch with Celery, add the following to your settings file:

```python
INSTALLED_APPS = [
    ...
    'csf.ranch'
]

RANCH = {
    'env': ENV_NAME,  # e.g. production, development
    'service': MY_SERVICE_NAME,  # e.g. backend
}
```

## Features

### Metrics

Any application with Ranch installed will have Celery metrics available in [the Celery/Ranch Datadog Dashboard](https://app.datadoghq.com/dashboard/hre-8ng-ywv/celery).

### Monitors
You may set up monitors for your application using the metrics provided by Ranch.

### Dead Letter Queue

Celery jobs that fail will be stored in the application's database for inspection and reprocessing. Ranch provides an Admin interface for this.

See [backends's Ranch Admin](https://api.constrafor.com/constrafor-admin/ranch/loggedtask/) for an example.

### Correlation IDs

Ranch can flow correlation IDs through your Celery jobs. Ranch will *not* change any of your logging configuration, so you'll still need to do that as part of your correlation ID implementation.

To use the correlation ID functionality, add the following settings:

```python
RANCH = {
    ...,
    'correlation': {
        'getter': getter_fn,  # callable with no args that returns the current correlation ID
        'setter': setter_fn,  # callable with one arg which should be set as the current correlation ID
    },
}
```

### Supplemental Error Tagging

Ranch provides a hook to add additional tagging information to error item metrics.

To use this feature, add the following settings:

```python
RANCH = {
    ...,
    # tags_fn takes a single arg (the Ranch Task object that failed)
    # and should return a list of strings in the format "tag_name:tag_value"
    'extra_error_queue_tags_fn': tags_fn,
}
```