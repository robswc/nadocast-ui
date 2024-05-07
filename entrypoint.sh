#!/bin/bash

# run the dash app with gunicon
exec gunicorn -b :5000 app:server