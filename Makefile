-include secrets.mk
PROJECT_DIR:=/app/gentilmechant

deploy:
	yarn build
	rsync -av -e ssh --exclude-from='.dockerignore' ./ $(USER)@$(HOST):$(PROJECT_DIR)
	ssh $(USER)@$(HOST) 'cd $(PROJECT_DIR) && docker compose up --build --force-recreate --remove-orphans -d'
	$(MAKE) logs

dev:
	./dev.sh

stop:
	ssh $(USER)@$(HOST) 'cd $(PROJECT_DIR) && docker compose stop'

start:
	ssh $(USER)@$(HOST) 'cd $(PROJECT_DIR) && docker compose start'

shell:
	ssh $(USER)@$(HOST) 'cd $(PROJECT_DIR) && docker compose exec -it gentilmechant sh'

logs:
	ssh $(USER)@$(HOST) 'cd $(PROJECT_DIR) && docker compose logs -f gentilmechant'

ssh:
	ssh $(USER)@$(HOST)

.PHONY: deploy shutdown start