FROM registry1.dso.mil/ironbank/opensource/python/python39:v3.9.16

WORKDIR /home/python

COPY --chown=python:python . .

ENV PYTHONPATH=/home/python/.cache/python-packages

ENTRYPOINT ["./entrypoint.sh"]

CMD ["python", "-m", "gunicorn", "-b", "0.0.0.0:8080", "app:create_app()"]
