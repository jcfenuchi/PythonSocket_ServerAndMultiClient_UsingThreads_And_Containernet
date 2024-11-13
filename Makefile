.PHONY: help
help: ## this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  \033[36m\033[0m\n"} /^[$$()% a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: run
setup: ## run main code
@echo "running main code"
	sudo python3 main.py


.PHONY: build
setup: ## build images
	@echo "building the docker images"
	docker build -f Minion/dockerfile -t minion:1.0 ./Minion
	docker build -f Core/dockerfile -t core:1.0 ./Core

.PHONY: cleanup
clear: ## clean_environment
	@echo "cleaning docker the images"
	docker rmi minion:1.0 2>/dev/null
	docker rmi core:1.0 2>/dev/null