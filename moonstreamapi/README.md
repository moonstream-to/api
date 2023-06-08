# moonstream backend

### Installation and setup

To set up Moonstream API for development, do the following:

- Clone the git repository
- Install postgresql (https://www.postgresql.org/download/linux/ubuntu/)

#### Run server with Docker

To be able to run Moonstream API with your existing local or development services as database, you need to build your own setup. **Be aware! The files with environment variables `docker.dev.env` lives inside your docker container!**

- Copy `configs/sample.env` to `configs/docker.dev.env`, or use your local configs from `configs/dev.env` to `configs/docker.dev.env`
- Edit in `docker.dev.env` file `MOONSTREAM_DB_URI` and other variables if required
- Clean environment file from `export ` prefix and quotation marks to be able to use it with Docker

```bash
sed --in-place 's|^export * ||' configs/docker.dev.env
sed --in-place 's|"||g' configs/docker.dev.env
```

Build container on your machine

```bash
docker build -t moonstreamapi-dev .
```

Run `moonstreamapi-dev` container, with following command we specified `--network="host"` setting which allows to Docker container use localhost interface of your machine (https://docs.docker.com/network/host/)

```bash
docker run --name moonstreamapi-dev \
  --network="host" \
  --env-file="configs/docker.dev.env" \
  -p 7481:7481/tcp \
  -ti -d moonstreamapi-dev
```

Attach to container to see logs

```bash
docker container attach moonstreamapi-dev
```
