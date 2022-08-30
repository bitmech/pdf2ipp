FROM python:slim-buster
ADD . /app
RUN pip install -r /app/requirements.txt && \
    apt-get update && apt-get install -y --no-install-recommends \
	lpr \
    cups \
    cups-client \
    cups-pdf \
	netcat \
	&& rm -rf /var/lib/apt/lists/*
CMD ["/app/start.sh"]
