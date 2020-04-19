install:
	pip install -r requirements.txt

test:
	pytest ./tests

test-with-coverage:
	py.test tests --cov=pymonet

lint:
	flake8 ./pymonet ./tests ./testers --max-line-length=120

lint-docs:
	pydocstyle ./pymonet --add-ignore=D100,D101,D102,D103,D104,D105,D107,D200,D205,D400,D401

type-check:
	mypy pymonet

check:
	(make lint & make lint-docs & make test) && echo "Success!"

generate-docs:
	sphinx-build -b html . docs/dist

clean-docs:
	rm -rf docs/dist

publish-pip:
	python setup.py sdist upload