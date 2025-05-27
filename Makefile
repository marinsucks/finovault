NAME = finovault

DEFAULT_DIR = ./testdata

all: build
	@if [ -z "$$FINOVAULT_DIR" ]; then \
		echo "$(BRED)FINOVAULT_DIR$(RED) environment variable not set.$(RESET)"; \
		export FINOVAULT_DIR=$(DEFAULT_DIR); \
	fi; \
	echo "$(YELLOW)Using directory: $(BYELLOW)$$(realpath $${FINOVAULT_DIR})$(RESET)"; \
	docker run --rm -d \
		-p 5000:5000 \
		-v $$(realpath $${FINOVAULT_DIR}):/data \
		-e DIR_NAME=$$(realpath $${FINOVAULT_DIR}) \
		--name finovault \
		finovault
	@echo "$(BGREEN)$(NAME) is running!$(GREEN) Access it at $(BGREEN)http://localhost:5000$(GREEN) or stop it with $(BGREEN)make stop$(RESET)"

stop:
	@echo "$(RED)Stopping $(BRED)$(NAME)$(RED)...$(RESET)"
	@docker stop $(shell docker ps -q --filter ancestor=$(NAME)) || true
	@docker rm -f $(shell docker ps -aq --filter ancestor=$(NAME)) || true

build:
	@echo "$(YELLOW)Building $(BYELLOW)$(NAME)$(YELLOW)...$(RESET)"
	@docker build -t $(NAME) .

re: stop all

.PHONY: all stop build re

# COLORS
RED = \033[0;31m
BRED = \033[1;31m
GREEN = \033[0;32m
BGREEN = \033[1;32m
YELLOW = \033[0;33m
BYELLOW = \033[1;33m
BLUE = \033[0;34m
BBLUE = \033[1;34m
MAGENTA = \033[0;35m
BMAGENTA = \033[1;35m
CYAN = \033[0;36m
BCYAN = \033[1;36m
WHITE = \033[0;37m
BWHITE = \033[1;37m
RESET = \033[0m
