#!/bin/sh

echo "Waiting for database..."
while ! python -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('db', 5432))
s.close()
" 2>/dev/null; do
  sleep 1
done
echo "Database is ready!"

python manage.py makemigrations
python manage.py migrate --no-input
python manage.py runserver 0.0.0.0:8000
