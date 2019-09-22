RapidPro Stack
===============
A complete RapidPro stack; including courier.

* To build and run the server

```
sudo docker-compose -f main.yml up --build
```

* Once up and running you can access Rapidpro from your browser as follows;

```
https://localhost
```

* RapidPro environment variables are available on the file, `rapidpro.env`.


* To remove all containers

```
sudo docker-compose rm -fsv
```
