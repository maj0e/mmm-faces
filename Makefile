MAGICMIRROR_IMAGE?="bastilimbach/docker-magicmirror"
TARGET_ARCH="x64"

.PHONY: help clean test-in-magic-mirror 
.DEFAULT_GOAL := help


help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean:
	find . | grep -E '(__pycache__|\.pyc|\.pyo$$)' | xargs rm -rf
	rm -r deploy/build
	mkdir deploy/build

purge: clean
	docker rmi CrossCompileEnv

test-in-magic-mirror:
	docker run  -d \
    --publish 80:8080 \
    --restart always \
    --volume $(pwd)/tests/config:/opt/magic_mirror/config \
    --volume $(pwd)/tests/modules:/opt/magic_mirror/modules \
    --name magic_mirror \
    ${MAGICMIRROR_IMAGE}

create-dockcross:
	- docker build --tag crosscompileenv deploy/platforms
	- docker run crosscompileenv > ./deploy/build/CrossCompileEnv
	- chmod +x CrossCompileEnv

build-opencv: create-dockcross 
	./deploy/build/CrossCompileEnv ./deploy/build_ocv.sh

build-dlib: create-dockcross 
	./deploy/build/CrossCompileEnv ./deploy/build_dlib.sh

test:
	pytest tests/

test-parallel:
	pytest --workers auto tests/

build-cpu: 
	docker build -t ${CPU_IMAGE} .

build-gpu:
	docker build -t ${GPU_IMAGE} . --build-arg gpu_tag="-gpu"

build-cpu-if-not-built: 
	if [ ! $$(docker images -q ${CPU_IMAGE}) ]; then $(MAKE) build-cpu; fi;

build-gpu-if-not-built: 
	if [ ! $$(docker images -q ${GPU_IMAGE}) ]; then $(MAKE) build-gpu; fi;

run-notebook: build-cpu-if-not-built
	docker run -it --rm -p=8888:8888 ${CPU_IMAGE} jupyter notebook --ip='*' --port=8888 --no-browser --allow-root ./examples/

run-tests: build-cpu-if-not-built
	docker run -it --rm ${CPU_IMAGE} make test

run-notebook-gpu: build-gpu-if-not-built
	docker run -it --rm -p=8888:8888 ${GPU_IMAGE} jupyter notebook --ip='*' --port=8888 --no-browser --allow-root /examples/

run-docs-gpu: build-gpu-if-not-built
	if [ $$(docker ps -aq --filter name=tensortrade_docs) ]; then docker rm $$(docker ps -aq --filter name=tensortrade_docs); fi;
	docker run -t --name tensortrade_docs ${GPU_IMAGE} make docs-build && make docs-serve
	python3 -m webbrowser http://localhost:8000/docs/build/html/index.html

run-tests-gpu: build-gpu-if-not-built
	docker run -it --rm ${GPU_IMAGE} make test

package:
	rm -rf dist
	python3 setup.py sdist
	python3 setup.py bdist_wheel

test-release: package
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

release: package
	twine upload dist/*
