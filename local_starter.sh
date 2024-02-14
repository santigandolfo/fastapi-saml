#!/bin/sh
uvicorn src.main:app --ssl-keyfile=key.pem --ssl-certfile=cert.pem --host=0.0.0.0 --port=8000 --reload
