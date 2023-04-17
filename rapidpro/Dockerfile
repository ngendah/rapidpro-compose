FROM python:3.9-slim as base-py3.9
ARG RAPIDPRO_VERSION
RUN set -ex \
      && apt-get update \
      && apt-get install -y --no-install-recommends nodejs npm libxml2 libpcre3 openssl libgeos-dev \
      && npm install -g coffeescript less
RUN set -ex \
      && addgroup --system rapidpro \
      && adduser --system --ingroup rapidpro rapidpro
USER rapidpro
WORKDIR /home/rapidpro
RUN set -ex \
      && python3 -m venv /home/rapidpro \
      && pip install -U pip setuptools \
      && pip install --user poetry
ENV PATH="/home/rapidpro/.local/bin:$PATH"

FROM base-py3.9 AS build-py3.9
USER root
RUN set -ex \
        && apt-get update \
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

FROM base-py3.9
USER root
RUN set -ex \
      && apt-get install -y gdal-bin supervisor postgresql-client
USER rapidpro
COPY --chown=rapidpro:rapidpro --from=build-py3.9 /home/rapidpro/.cache/ .cache/
COPY --chown=rapidpro:rapidpro --from=build-py3.9 /home/rapidpro/.local/ .local/
COPY --chown=rapidpro:rapidpro --from=build-py3.9 /home/rapidpro/bin/ bin/
COPY --chown=rapidpro:rapidpro --from=build-py3.9 /home/rapidpro/app/ app/
WORKDIR app
COPY stack/settings.py ./temba
COPY startup.sh ./
COPY supervisor.conf ./
EXPOSE 8000 8080
ENTRYPOINT ["./startup.sh"]
