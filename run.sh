#!/bin/bash

# 1024 - 65535
source env/bin/activate
uvicorn src.app:asgi_app --reload --host 127.0.0.1 --port 23008 --reload