ISORT_ARGS="--line-length 79"

all: fmt

lint:
	isort ${ISORT_ARGS} .
	black --diff .

fmt:
	isort ${ISORT_ARGS} .
	black --safe .

.PHONY: lint fmt
