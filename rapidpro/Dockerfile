FROM python:3.10-bookworm AS rapidpro-base
ARG RAPIDPRO_VERSION
RUN set -ex \
      && apt-get update \
      && apt-get install -y --no-install-recommends \
                nodejs \
                npm \
                libxml2 \
                libpcre3 \
                openssl libgeos-dev \
      && npm install -g coffeescript less \
      && addgroup --system rapidpro \
      && adduser --system --ingroup rapidpro rapidpro
RUN set -ex \
      && pip install --no-cache-dir poetry
USER rapidpro
WORKDIR /home/rapidpro
ENV POETRY_VIRTUALENVS_PATH=/home/rapidpro

FROM rapidpro-base AS rapidpro-build
USER root
RUN set -ex \
        && apt-get install -y \
                wget \
                build-essential \
                libpq-dev \
                libjpeg-dev \
                libpng-dev \
                libfreetype-dev \
                libxslt-dev \
                libxml2-dev \
                zlib1g-dev \
                libffi-dev \
                libpcre2-dev \
                libreadline-dev \
                libncurses-dev \
                libgdal-dev \
               libzmq3-dev
USER rapidpro
RUN mkdir app
RUN set -ex \
      && export HOME=/home/rapidpro \
      && export RAPIDPRO_VERSION="v$RAPIDPRO_VERSION" \
      && export RAPIDPRO_REPO_URL="https://github.com/rapidpro/rapidpro/archive/$RAPIDPRO_VERSION.tar.gz" \
      && echo "Downloading RapidPro $RAPIDPRO_VERSION from $RAPIDPRO_REPO_URL" \
      && wget -q -O rapidpro.tar.gz $RAPIDPRO_REPO_URL \
      && tar -C app -xf rapidpro.tar.gz --strip-components=1 \
      && rm rapidpro.tar.gz \
      && export CRYPTOGRAPHY_DONT_BUILD_RUST=1 \
      && cd app \
      && mkdir .npm \
      && npm install \
      && poetry install --without dev --sync

FROM rapidpro-base
USER root
RUN set -ex \
      && apt-get install -y gdal-bin wget postgresql-client
USER rapidpro
ENV HOME=/home/rapidpro
COPY --chown=rapidpro:rapidpro --from=rapidpro-build /home/rapidpro/ .
WORKDIR app
COPY --chown=rapidpro:rapidpro stack/settings.py ./temba/
COPY --chown=rapidpro:rapidpro stack/admin.py ./temba/orgs/management/commands/
COPY --chown=rapidpro:rapidpro server.sh celery.sh ./
EXPOSE 8000 8080
ENTRYPOINT ["/bin/sh"]
CMD ["-c", "./server.sh"]
