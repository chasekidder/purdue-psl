#!/bin/bash
celery -A src.measure worker --loglevel=INFO
