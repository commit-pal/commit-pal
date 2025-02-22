.PHONY: lint publish

lint:
	cd cmpal && poetry run black .
	cd cmpal && poetry run isort .
	cd cmpal && poetry run autoflake --in-place --remove-all-unused-imports --recursive .

publish:
	poetry build
	poetry publish
