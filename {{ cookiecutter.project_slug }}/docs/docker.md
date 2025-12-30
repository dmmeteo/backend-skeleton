## Docker

To start project faster we use docker and docker compose. In docker compose file we have all services that we need to
run, some of them mapped to local ports, so we can access them from the host machine.
You can change default ports by create `.env` file in `docker` directory and set variables with the same name as in
`docker-compose.yml` file.

Example of `.env` file:

```dotenv
API_LOCAL_PORT=8099 # change default port for api service from 8000 to 8099
```

## Services

### api

The `api` service is responsible for running django application.
The api service has the following configurations:

 - Command: `make run` (runs the API, see `api/Makefile` for details)
 - Ports: `${LOCAL_IP:-127.0.0.1}:${API_LOCAL_PORT:-8000}:8000` (by default maps http://localhost:8000 to the API container)
 - Environment File: `../api/.env` (loads environment variables from the specified file)
 - Volumes: `../api:/opt/api` (mount `api` directory to `/opt/api` in the container, to make
sure that we have the same code in the container and on the host machine for development purposes.)

#### api build
 - Target `local` is used to build image for local development, check `docker/images/api/Dockerfile` for details.
 - Target `live` is used to build image for production. `docker/images/api/Dockerfile` - is production ready, but docker
   compose configuration only for local development.


### celery-worker

The `celery-worker` service is responsible for running the Celery worker. It uses same image as `api` service,
but instead of starting web server, it starts celery worker.

 - Command: `make celery-worker-run` (check `api/Makefile` for details)

### celery-beat

The `celery-beat` service is responsible for running the Celery beat scheduler.

 - Command: `make celery-beat-run` (check `api/Makefile` for details)


### postgres-db

The `postgres-db` service is a PostgreSQL database service.


### redis-db

The `redis-db` service is a Redis database service.

### mailpit

The `mailpit` service is an instance of the Mailpit email testing tool. It has the following configurations:

- Ports: `${LOCAL_IP:-127.0.0.1}:${MAILPIT_LOCAL_PORT:-8025}:8025` (by default maps http://localhost:8025 to the Mailpit container)

### rustfs

The `rustfs` service is an instance of [RustFS](https://rustfs.com/) - a high-performance, S3-compatible object storage
system built in Rust. We store static and media files there. RustFS is a drop-in replacement for MinIO with better
performance and Apache 2.0 license.

It has the following configurations:
- Ports:
  - `${LOCAL_IP:-127.0.0.1}:${RUSTFS_LOCAL_PORT:-9000}:9000` (maps RustFS API to the local IP and port)
  - `${LOCAL_IP:-127.0.0.1}:${RUSTFS_CONSOLE_LOCAL_PORT:-9001}:9001` (maps RustFS Console UI to the local IP and port)
- Environment variables: `RUSTFS_ACCESS_KEY` and `RUSTFS_SECRET_KEY` for authentication.
- Default credentials: `rustfsadmin` / `rustfsadmin`

RustFS Console (UI) is available at http://localhost:9001 by default.

### createbuckets

This service creates default buckets in RustFS for storing static and media files using
[MinIO Client (mc)](https://min.io/docs/minio/linux/reference/minio-mc.html). RustFS officially supports mc -
see [RustFS mc documentation](https://docs.rustfs.com/developer/mc.html).

The service:
1. Waits for RustFS to be available
2. Creates an alias `myrustfs` pointing to the RustFS instance
3. Creates a bucket for storing files
4. Sets anonymous download policy on the bucket



## Extra services that can be useful
We didn't add these services by default, do not overload compose file.

#### pgadmin
The `pgadmin` service is an instance of the pgAdmin - PostgreSQL database management tool with nice UI that allow you to
check database, tables, run queries, etc.

```yaml
services:
  pgadmin:
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_DEFAULT_EMAIL:-pgadmin4@example.com}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_DEFAULT_PASSWORD:-admin}
    ports:
      - ${LOCAL_IP:-127.0.0.1}:${PGADMIN_LOCAL_PORT:-5050}:80
    volumes:
      - pgadmin_data:/var/lib/pgadmin
volumes:
  pgadmin_data: {}
```

#### redisinsight

The `redisinsight` service is an instance of the RedisInsight - the Redis GUI, super useful to debug Redis.

```yaml
services:
  redisinsight:
    image: redislabs/redisinsight:latest
    ports:
      - ${LOCAL_IP:-127.0.0.1}:${REDISINSIGHT_LOCAL_PORT:-8001}:8001
    volumes:
    - redisinsight_data:/db
volumes:
  redisinsight_data: {}
```

#### flower

The `flower` service is an instance of the Flower - the Celery monitoring tool.

```yaml
services:
  flower:
    image: mher/flower:0.9.7
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - FLOWER_PORT=5555
    ports:
      - ${LOCAL_IP:-127.0.0.1}:${FLOWER_LOCAL_PORT:-5555}:5555
    depends_on:
      - redis
```
