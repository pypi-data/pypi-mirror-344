default : upload-test

upload-test : build
	python3 -m twine upload --repository testpypi dist/*

upload : build
	python3 -m twine upload dist/*

build :
	python3 -m build
