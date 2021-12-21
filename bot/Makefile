ifeq ($(TG_TOKEN),)
	export TG_TOKEN = "1234:faketoken"
endif
ifeq ($(KINO_TOKEN),)
	export KINO_TOKEN="1234:faketoken"
endif

build:
	docker-compose build bot

up:
	docker-compose up -d bot

down:
	docker-compose stop
	docker-compose down

run:
	make down
	docker-compose build bot
	docker-compose up -d bot
	docker-compose logs -f
