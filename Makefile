ifneq (,$(wildcard ./.env.dev))
    include .env.dev
    export
endif

build-image:
	docker build . -t ${IMAGE_NAME}

start:
	docker run --name "${CONTAINER_NAME}" --detach --rm "${IMAGE_NAME}"

lint-check:
	docker exec "${CONTAINER_NAME}" pixi run --environment dev lint-check

format-check:
	docker exec "${CONTAINER_NAME}" pixi run --environment dev format-check

types-check:
	docker exec "${CONTAINER_NAME}" pixi run --environment dev types-check

order-imports-check:
	docker exec "${CONTAINER_NAME}" pixi run --environment dev order-imports-check

connect:
	docker run --name ${CONTAINER_NAME} -it ${IMAGE_NAME} --entrypoint /bin/bash

stop:
	docker stop "${CONTAINER_NAME}"

rm-all-containers:
	docker rm $(docker ps --quiet --all)

test:
	pixi run test
