ISORT_ARGS="--line-length 79"

all: fmt-setup lint fmt

lint:
	isort ${ISORT_ARGS} .
	black --diff .

fmt-setup:
	isort ${ISORT_ARGS} .
	black --safe .

.PHONY: lint fmt
