up:
	docker-compose up -d

down:
	docker-compose down

run:
	python3 resolver.py

test:
	python test_resolver.py

.PHONY: all $(MAKECMDGOALS)