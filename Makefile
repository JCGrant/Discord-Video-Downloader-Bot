APP_NAME=scout-bot
IMAGE_NAME=jcgrant/$(APP_NAME)

run:
	uv run src/main.py

docker-build:
	docker build -t $(IMAGE_NAME) .

docker-push:
	docker push $(IMAGE_NAME)

prod-logs:
	kubectl logs -f -l app=$(APP_NAME)

prod-shell:
	kubectl exec -it $$(kubectl get pods | grep "${APP_NAME}" | awk '{print $$1}' | head -n 1) -- /bin/sh

prod-restart:
	kubectl delete pod $$(kubectl get pods | grep "${APP_NAME}" | awk '{print $$1}' | head -n 1) --grace-period=0

prod-deploy: docker-build docker-push prod-restart
