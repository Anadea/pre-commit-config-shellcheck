FROM python:3.10.5-slim

ENV PRE_COMMIT_CONFIG_SHELLCHECK_VERSION="0.2.1"
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
    python -m pip install pre-commit-config-shellcheck=="${PRE_COMMIT_CONFIG_SHELLCHECK_VERSION}"

# switch user, workdir, and setup entrypoint
USER app
WORKDIR /opt/app
ENTRYPOINT ["/opt/app/entrypoint.sh"]
