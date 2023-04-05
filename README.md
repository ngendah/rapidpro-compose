RapidPro v7 stack with docker compose
=====================================

![Build Status](https://github.com/ngendah/rapidpro-compose/actions/workflows/linux.yaml/badge.svg)


[RapidPro](https://github.com/rapidpro/rapidpro) is an interactive SMS builder which offers an intuitive UI for working with SMS workflows involving crafting, sending, receiving and processing SMS'es.

It's stack is composed of various services which need to be started separately and this can be challenging when trying to self host or running it locally on your machine.

This project simplifies the process by consolidating it's main services to a single configuration file easily started by a single command.


To start you will need build and run the servers as follows;

#### On Linux

1. Install [git](https://github.com/git-guides/install-git), [docker](https://docs.docker.com/engine/), [docker compose](https://docs.docker.com/compose/) and confirm that docker is running.

2. Clone the project.

```
git clone https://github.com/ngendah/rapidpro-compose.git
```

3. Change your active directory to the cloned directory.

4. Build the images and start compose.

```
docker compose up --build
```

5. Once running you can access Rapidpro from your browser.

```
https://localhost
```

&nbsp;&nbsp;&nbsp;&nbsp;e.g `https://localhost`

>> Because the server is using a self-signed SSL/TLS certificate, the browser will issue a warning. Ignore the warning and continue. e.g on Firefox, click on `advanced` button and accept.

#### On Windows 10

1. Install [git](https://github.com/git-guides/install-git), [docker](https://docs.docker.com/engine/install/), [docker compose](https://docs.docker.com/compose/install/) and confirm that docker is running.

>> While installing git configure it's line-endings conversion to use unix-style line endings.

2. Start the `git-bash console` installed on the desktop.

3. Clone the project.

```
git clone https://github.com/ngendah/rapidpro-compose.git
```

4. Change your active directory to the cloned directory.

```
cd rapidpro
```

5. Build the images.

```
docker compose build
```

6. Start the composer

```
docker compose up
```

7. Once running you can access Rapidpro from your browser.

```
https://localhost
```

&nbsp;&nbsp;&nbsp;&nbsp;e.g `https://localhost`

>> Because the server is using a self-signed SSL/TLS certificate, the browser will issue a warning, ignore the warning and continue. e.g on Firefox, click on `advanced` button and accept.


### NOTES

1. The stack environment variables are available on the file `rapidpro.env`.

2. To add elastic search visit the official guide [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html)

3. RapidPro development guides are available [here](http://rapidpro.github.io/rapidpro/).


### CREDITS

1. [RapidPro](https://github.com/rapidpro/rapidpro) project.

2. [Praekelt.org](https://github.com/praekeltfoundation) for the initial docker base images for [mailroom](https://github.com/praekeltfoundation/mailroom-docker) and [courier](https://github.com/praekeltfoundation/courier-docker).
