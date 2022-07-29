FROM python:3.10.5-slim AS compile-image

ENV VIRTUAL_ENV="/opt/.env"
ENV PATH="/opt/app:${VIRTUAL_ENV}/bin:${PATH}"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# create user
RUN set -eaux pipefail; \
    useradd -m -U -r app

# copy package files
COPY . /opt/app

# install package
RUN set -eaux pipefail; \
    python -m venv "${VIRTUAL_ENV}"; \
    python -m pip install pip wheel --upgrade; \
    python -m pip install /opt/app

# switch user, workdir, and setup entrypoint
USER app
WORKDIR /opt/app
ENTRYPOINT ["entrypoint.sh"]
