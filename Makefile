NAME = finovault

FINOVAULT_DATA = ./testdata

all: build
	@if [ "$(FINOVAULT_DATA)" = "tests/data" ]; then \
		echo "$(YELLOW)Using default data directory: $(BYELLOW)$(FINOVAULT_DATA)$(RESET)"; \
		echo "$(YELLOW)To use your own data directory, run:$(RESET)"; \
		echo "$(BYELLOW)  make FINOVAULT_DATA=/yourdatahere$(RESET)"; \
	fi
	@docker run \
		-p 5000:5000 \
    	-v $(FINOVAULT_DATA):/data \
    	finovault

build:
	@echo "$(GREEN)Building $(BGREEN)$(NAME)$(GREEN)...$(RESET)"
	@docker build -t $(NAME) .


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
