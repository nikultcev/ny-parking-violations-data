SHELL := /bin/sh
.PHONY: all

include .env
export

all: create-venv install terraform-init terraform-apply docker-build docker-up
windows: create-venv-windows install-windows terraform-init terraform-apply docker-build docker-up

create-venv:
	@echo "Creating virtual environment..."
	python3 -m venv .venv
	@echo "Virtual environment created in .venv"

create-venv-windows:
	@echo "Creating virtual environment..."
	python -m venv .venv
	@echo "Virtual environment created in .venv"

install: 
	@echo "Installing dependencies"
	.venv/bin/pip install -r requirements.txt

install-windows:
	@echo "Installing dependencies"
	.venv/Scripts/pip.exe install -r requirements.txt

terraform-init:
	cd terraform && terraform init

terraform-plan:
	cd terraform && terraform plan \
		-var="google_cloud_storage_location=$(GOOGLE_CLOUD_STORAGE_LOCATION)" \
		-var="google_region=$(GOOGLE_REGION)" \
		-var="google_project=$(GOOGLE_PROJECT)" \
		-var="google_cloud_storage_bucket=$(GOOGLE_CLOUD_STORAGE_BUCKET)"

terraform-apply:
	cd terraform && terraform apply \
		-var="google_cloud_storage_location=$(GOOGLE_CLOUD_STORAGE_LOCATION)" \
		-var="google_region=$(GOOGLE_REGION)" \
		-var="google_project=$(GOOGLE_PROJECT)" \
		-var="google_cloud_storage_bucket=$(GOOGLE_CLOUD_STORAGE_BUCKET)"

dbt-test:
	cd dbt && dbt seed && dbt test

dbt-debug:
	cd dbt && dbt debug

dbt-run:
	cd dbt && dbt seed && dbt run

docker-build:
	docker compose build

docker-up:
	docker compose up -d && docker exec -it airflow-scheduler /bin/bash -c "airflow connections import plugins/airflow_connections.json"