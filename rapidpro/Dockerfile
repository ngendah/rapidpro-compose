FROM python:3.9-slim as rapidpro-base-py3.9
ARG RAPIDPRO_VERSION
RUN apt-get update; \
    apt-get install -y --no-install-recommends nodejs npm libxml2 libpcre3 \
    openssl gdal-bin libgeos-dev supervisor postgresql-client
RUN npm install -g coffeescript less
WORKDIR /home/root
ENV HOME=/home/root
RUN python3 -m venv /usr/local/bin/
RUN pip install -U pip setuptools
RUN pip install poetry

FROM rapidpro-base-py3.9 AS rapidpro-3.9-build
WORKDIR /home/root
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
ENV RAPIDPRO_VERSION="v$RAPIDPRO_VERSION"
ENV RAPIDPRO_REPO=${RAPIDPRO_REPO:-rapidpro/rapidpro}
ENV RAPIDPRO_REPO_URL="https://github.com/$RAPIDPRO_REPO/archive/$RAPIDPRO_VERSION.tar.gz"
RUN echo "Downloading RapidPro $RAPIDPRO_VERSION from $RAPIDPRO_REPO_URL" \
    && wget -q -O rapidpro.tar.gz $RAPIDPRO_REPO_URL \
    && mkdir rapidpro \
    && tar -C rapidpro -xf rapidpro.tar.gz --strip-components=1 \
    && rm rapidpro.tar.gz
WORKDIR /home/root/rapidpro/
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN mkdir .npm
RUN npm install
RUN poetry install

FROM rapidpro-base-py3.9 AS rapidpro
WORKDIR $HOME
RUN rm -rf $HOME/.cache $HOME/.local
COPY --from=rapidpro-3.9-build $HOME/.cache/ $HOME/.cache/
COPY --from=rapidpro-3.9-build $HOME/.local/ $HOME/.local/
COPY --from=rapidpro-3.9-build $HOME/rapidpro/ $HOME/rapidpro/
WORKDIR $HOME/rapidpro/
COPY stack/settings.py ./temba
COPY startup.sh ./
COPY supervisor.conf ./
EXPOSE 8000 8080
ENTRYPOINT ["./startup.sh"]
