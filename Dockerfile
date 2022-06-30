FROM registry1.dso.mil/ironbank/opensource/python/python39:v3.9.13

WORKDIR /home/python

COPY --chown=python:python . .

ENV PYTHONPATH=/home/python/.cache/python-packages

ENTRYPOINT ["./entrypoint.sh"]
