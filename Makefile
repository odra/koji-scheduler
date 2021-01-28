SHELL = /bin/bash
IMAGE = quay.io/lrossett/koji-builder-kube:latest

test: test/code test/unit

test/code:
	@poetry run mypy src/koji_builder_kube --strict

test/unit:
	@poetry run pytest

image/build:
	docker build -t ${IMAGE} .

image/debug:
	docker run -it --entrypoint /bin/bash ${IMAGE}

image/push:
	docker push ${IMAGE}

.PHONY: test test/code test/unit image/build image/debug image/push