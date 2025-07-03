FROM python:3.10-bookworm AS rapidpro-base
ARG RAPIDPRO_VERSION
RUN set -ex \
  && apt-get update \
  && apt-get install -y --no-install-recommends \
       nodejs \
       npm \
       libxml2 \
       libpcre3 \
       openssl \
       libgeos-dev \
       gdal-bin \
       wget \
       postgresql-client \
  && npm install -g coffeescript less \
  && addgroup --system rapidpro \
  && adduser --system --ingroup rapidpro rapidpro \
  && pip install --no-cache-dir poetry \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER rapidpro
WORKDIR /home/rapidpro
ENV POETRY_VIRTUALENVS_PATH=/home/rapidpro
ENV HOME=/home/rapidpro

FROM rapidpro-base AS rapidpro-build
USER root
RUN set -ex \
  && apt-get update \
  && apt-get install -y --no-install-recommends \
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
       libzmq3-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER rapidpro
RUN set -ex \
  && mkdir app \
  && wget -q -O rapidpro.tar.gz "https://github.com/rapidpro/rapidpro/archive/v${RAPIDPRO_VERSION}.tar.gz" \
  && tar -C app -xf rapidpro.tar.gz --strip-components=1 \
  && rm rapidpro.tar.gz \
  && cd app \
  && mkdir .npm \
  && npm install \
  && poetry install --without dev --sync \
  && find $HOME -type d -name '.*' -prune -exec rm -rf {} +;

FROM rapidpro-base
COPY --from=rapidpro-build /home/rapidpro/ /home/rapidpro/
WORKDIR app
COPY stack/settings.py ./temba/
COPY stack/admin.py ./temba/orgs/management/commands/
COPY server.sh celery.sh ./
EXPOSE 8000 8080
ENTRYPOINT ["/bin/sh"]
CMD ["-c", "./server.sh"]

