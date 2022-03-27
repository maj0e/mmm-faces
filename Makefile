MAGICMIRROR_IMAGE?="bastilimbach/docker-magicmirror"
TARGET_ARCH="x64"
BUILD_DIR= deploy/build

.PHONY: help clean test-in-magic-mirror 
.DEFAULT_GOAL := help


help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean:
	find . | grep -E '(__pycache__|\.pyc|\.pyo$$)' | xargs rm -rf
	rm -r ${BUILD_DIR}
	mkdir ${BUILD_DIR}


rm-container:
	docker stop magic_mirror
	docker rm magic_mirror

remove-image: rm-container
	docker image rm ${MAGICMIRROR_IMAGE}

purge: clean remove-image
	docker rmi CrossCompileEnv

start-magic-mirror: #rm-container ## Starts MagicMirror in Docker 
	- docker run -d \
    --publish 10205:8080 \
    --restart always \
    --volume $(shell pwd)/tests/config:/opt/magic_mirror/config \
    --volume $(shell pwd)/tests/modules:/opt/magic_mirror/modules \
    --name magic_mirror \
    ${MAGICMIRROR_IMAGE}
	- xdg-open http://127.0.0.1:10205

create-dockcross:
	- docker build --tag crosscompileenv deploy/platforms
	- docker run crosscompileenv > ${BUILD_DIR}/CrossCompileEnv
	- chmod +x ${BUILD_DIR}/CrossCompileEnv

build-opencv: create-dockcross 
	${BUILD_DIR}/CrossCompileEnv bash ./deploy/build_ocv.sh ${BUILD_DIR}
build-dlib: create-dockcross 
	${BUILD_DIR}/CrossCompileEnv ./deploy/build_dlib.sh ${BUILD_DIR}
	
build-module:# build-opencv build-dlib
	- ${BUILD_DIR}/CrossCompileEnv pyinstaller pythonFunctions

build: build-module ## Build the module and all dependencies

test:
	pytest tests/

