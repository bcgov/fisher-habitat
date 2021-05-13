psql:
	docker-compose exec db /bin/bash -c "psql postgres://fisher:test@localhost:5432/fisher"
