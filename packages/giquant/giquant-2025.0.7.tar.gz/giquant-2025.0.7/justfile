build:
	rm -rf dist
	rm -rf giquant.egg-info 
	python -m build

dist:
	twine upload dist/*

install:
	python3 -m pip install ./dist/giquant-2024.0.1.tar.gz
