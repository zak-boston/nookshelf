FROM python:3.12-slim

WORKDIR /app

# requests added for server-side status checks
RUN pip install flask requests --no-cache-dir

COPY app.py .
COPY static/ static/

EXPOSE 5001

CMD ["python", "app.py"]
