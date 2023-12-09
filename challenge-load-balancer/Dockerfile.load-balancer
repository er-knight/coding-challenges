FROM python:3.11-slim-bookworm

RUN python -m pip install colorama

COPY load-balancer.py .

CMD [ "python", "load-balancer.py"]