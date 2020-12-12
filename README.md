RapidPro v6 docker-compose Stack
=================================

[![Build Status](https://travis-ci.org/ngendah/rapidpro.svg?branch=master)](https://travis-ci.org/ngendah/rapidpro)

In order to build and run the server;

1. Install [git](https://github.com/git-guides/install-git), [docker](https://docs.docker.com/engine/install/) and [docker compose](https://docs.docker.com/compose/install/).

2. Clone the project in to your machine.

```
git clone https://github.com/ngendah/rapidpro.git
```

3. Change your active directory to the cloned direcory.

4. Build the images and start docker compose.

```
docker-compose up --build
```

5. Once up and running you can access Rapidpro from your browser as follows;

```
https://localhost
```

# NOTES

1. The build has not been tested on a windows machine.

2. RapidPro environment variables are available on the file, `rapidpro.env`.

3. To add elastic search visit the official guide [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html)

# CREDITS

1. [RapidPro](https://github.com/rapidpro/rapidpro) project.

2. [Nyaruka](https://github.com/nyaruka).
