FROM ubuntu:20.04 as base-py3.9
ARG RAPIDPRO_VERSION
RUN set -ex \
      && apt-get update \
      && apt-get install -y --no-install-recommends \
                python3.9 \
                python3-pip \
                python3.9-venv \
                nodejs \
                npm \
                libxml2 \
                libpcre3 \
                openssl libgeos-dev \
      && npm install -g coffeescript less \
      && addgroup --system rapidpro \
      && adduser --system --ingroup rapidpro rapidpro
USER rapidpro
WORKDIR /home/rapidpro
RUN set -ex \
      && python3.9 -m venv /home/rapidpro \
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
      && apt-get install -y gdal-bin wget postgresql-client
USER rapidpro
COPY --chown=rapidpro:rapidpro --from=build-py3.9 /home/rapidpro/.cache/ .cache/
COPY --chown=rapidpro:rapidpro --from=build-py3.9 /home/rapidpro/.local/ .local/
COPY --chown=rapidpro:rapidpro --from=build-py3.9 /home/rapidpro/bin/ bin/
COPY --chown=rapidpro:rapidpro --from=build-py3.9 /home/rapidpro/app/ app/
WORKDIR app
COPY --chown=rapidpro:rapidpro stack/settings.py ./temba
COPY --chown=rapidpro:rapidpro server.sh celery.sh ./
EXPOSE 8000 8080
ENTRYPOINT ["/bin/sh"]
CMD ["-c", "./server.sh"]
