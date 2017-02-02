init:
	pip install -r requirements.txt
clean:
	find . -name \*.pyc -delete
test:
	nosetests -v tests
try:
	python main.py
