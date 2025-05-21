FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir --upgrade pip setuptools wheel twine

ENV TWINE_REPOSITORY_URL=https://pypi.pkg.github.com

ENTRYPOINT ["bash", "-c", "python setup.py sdist bdist_wheel && twine upload dist/*"]
