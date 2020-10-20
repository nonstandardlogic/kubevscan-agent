PROJECT_NAME 	:= kubescan-agent

# ==============================================================================
# Building containers

FILES := $(shell docker ps -aq)

.PHONY: docker-build docker-push docker-stop docker-clean 

docker-build:
	docker build \
		-f Dockerfile \
		-t nonstandardlogic/$(PROJECT_NAME) \
		--build-arg BUILD_DATE=`date -u +"%Y-%m-%dT%H:%M:%SZ"` \
		.
docker-push:
	docker push nonstandardlogic/$(PROJECT_NAME)

docker-stop:
	docker stop $(FILES)
	docker rm $(FILES)

docker-clean:
	docker system prune -f	




