FROM registry1.dso.mil/ironbank/opensource/python:v3.10.11

USER python

WORKDIR /home/python

COPY --chown=python:python . .

ENV PYTHONPATH=/home/python/.cache/python-packages

ENTRYPOINT ["./entrypoint.sh"]

CMD ["python", "-m", "gunicorn", "-b", "0.0.0.0:8080", "app:create_app()"]
