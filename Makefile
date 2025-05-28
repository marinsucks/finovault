NAME = finovault

DEFAULT_DIR = ./tests/files

all: build
	@if [ -z "$$FINOVAULT_DIR" ]; then \
		echo "$(BRED)FINOVAULT_DIR$(RED) environment variable not set.$(RESET)"; \
		export FINOVAULT_DIR=$(DEFAULT_DIR); \
	fi; \
	echo "$(YELLOW)Using directory: $(BYELLOW)$${FINOVAULT_DIR}$(RESET)"; \
	test -d "$${FINOVAULT_DIR}" || { \
		echo "$(RED)Directory $(BRED)$${FINOVAULT_DIR}$(RED) does not exist.$(RESET)"; \
		exit 1; \
	}; \
	docker run -d \
		-p 5000:5000 \
		-v $$(realpath $${FINOVAULT_DIR}):/data \
		-e DIR_NAME=$$(realpath $${FINOVAULT_DIR}) \
		--name finovault \
		finovault
	@echo "$(BGREEN)$(NAME) is running!$(RESET)"
	@echo "$(GREEN)access:	$(BGREEN)http://localhost:5000$(GREEN)$(RESET)"
	@echo "$(YELLOW)tests:	$(BYELLOW)make tests$(RESET)"
	@echo "$(RED)stop:	$(BRED)make stop$(RESET)"

build:
	@echo "$(YELLOW)Building $(BYELLOW)$(NAME)$(YELLOW)...$(RESET)"
	@docker build -t $(NAME) .

stop:
	@echo "$(RED)Stopping $(BRED)$(NAME)$(RED)...$(RESET)"
	@docker stop $(shell docker ps -q --filter ancestor=$(NAME)) || true
	@docker rm -f $(shell docker ps -aq --filter ancestor=$(NAME)) || true

tests:
	@docker exec -e PYTHONPATH=/src -e PATH="/home/flaskuser/.local/bin:${PATH}" finovault pytest /tests/tests.py -v --color=yes

re: stop all

.PHONY: all build stop tests re

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
