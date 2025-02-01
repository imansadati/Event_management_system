# variables 
DOCKER = docker
DOCKER_COMPOSE = docker-compose
SERVICE = user_management # default
VENV = services/$(SERVICE)/venv/Scripts/activate


build:
	$(DOCKER_COMPOSE) up --build	

run:
	$(DOCKER_COMPOSE) up	

down:
	$(DOCKER_COMPOSE) down -v
	
log:
	$(DOCKER) logs $(SERVICE)

exec:
	docker exec -it $(SERVICE) bash

venv:
	@powershell -NoExit -Command "& { $(VENV) }"
