test:
	pytest -v

clear_cache:
	rm -rf .pytest_cache
	find . -type d -name "__pycache__" -exec rm -r {} \;

build:
	docker build -t kytobase .
	docker run -d -p 8000:5000 --name kytobase kytobase
