#!/usr/bin/env bash
# cd /usr/share/apk_reprepro/ || return
gunicorn -c gunicorn.py  wsgi:app 