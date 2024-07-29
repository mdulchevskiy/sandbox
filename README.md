# Sandbox

PROJECT DESCRIPTION

## Binaries requirements

### Docker:
    
- Install docker and compose v2 ([docker desktop installation](https://docs.docker.com/get-docker/)).

## Installation

1. Specify values for necessary environmental variables in `.env` file.

2. Copy database dump to specific environment folder.

   NOTE: use `dev` and `prod` folders for appropriate environments.

3. Specify database environment with environment variable `DATABASE_ENVIRONMENT` (the same values as in the previous step with database dump).

4. Recover database from dump (if hasn't been recovered yet):

    ```bash
    docker compose up sandbox-db-service
    ```

5. Build api service:

   NOTE: api service is used by collectstatic, migrator and celery services as image.
  
    ```bash
    docker compose build --no-cache sandbox-api-service
    ```

6. Apply migrations (wait until "*Custom migration finished!*" line):

    ```bash
    docker compose up sandbox-db-migrator-service
    ```

## Usage

1. Launch api service (database and redis services are launching automatically):

    ```bash
    docker compose up sandbox-api-service 
    ```

2. Launch celery workers with beat service (choose what is needed):
    ```bash
    docker compose up espresa-beat-service \
                      espresa-worker-cache-service \
                      espresa-worker-high-service \
                      espresa-worker-low-service \
                      espresa-worker-notification-service \
                      espresa-worker-payment-service
    ```