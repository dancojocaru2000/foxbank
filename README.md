# FoxBank

Project, Web Technologies, Year 3, Semester 1

## How to build

The design is modular: the client and the server can be hosted independently. This allows the client to be hosted on a static web host (for example GitHub Pages), and for the server to be hosted on another service. The client must know the address where the server is located.

### Client

Make sure to change the `baseURL` in `client/src/api.js`. The `baseURL` should point to the address of the server.

```js
const baseURL = "https://foxbank-api.extras.dcdevelop.xyz";
// or
const baseURL = "http://localhost:5000";
```

After changing the `baseURL`, build using the following commands:

```sh
cd client
npm install     # or yarn
npm run build   # or yarn run build
```

After running those commands, the `client/public` folder contains the client files to be deployed on the server.

### Server

The best way to deploy the server is using Docker:

```sh
cd server
docker build -t foxbank .
```

And then run the server using:

```sh
PORT=5000       # set port here
DATA_DIR=./data # set directory for server data here
docker run -p $PORT:5000 -v $DATA_DIR:/app/data foxbank
```

---

In order to ease the deployment of the server, [Docker Compose](https://docs.docker.com/compose/) can be used:

```sh
cd server
export PORT=5000 # set port here
docker-compose up -d
```

Check the `server/run.sh` script for further reference.

---

If you don't want to use Docker, use [`pipenv`](https://pipenv.pypa.io/en/latest/) to install the Python dependencies and run the project manually:

```sh
cd server
pipenv install
PORT=5000 # set port here
pipenv run gunicorn -b 0.0.0.0:$PORT server:app
```
