.PHONY: lint format test install

lint:
	cd cmp && poetry run black .
	cd cmp && poetry run isort .
	cd cmp && poetry run autoflake --in-place --remove-all-unused-imports --recursive .
