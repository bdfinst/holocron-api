FROM registry.il2.dso.mil/platform-one/devops/pipeline-templates/test-oci/python39:3.9.10-pbmd-3174

WORKDIR /home/python

COPY --chown=python:python . .

ENTRYPOINT ["./entrypoint.sh"]
