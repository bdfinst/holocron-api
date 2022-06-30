FROM registry1.dso.mil/ironbank/opensource/python/python39:v3.9.13

WORKDIR /home/python

COPY --chown=python:python . .

ENTRYPOINT ["./entrypoint.sh"]
