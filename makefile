python:
	python3 -B main.py

docker:
	docker build -t blkjk .

rd:
	docker run -it --rm blkjk