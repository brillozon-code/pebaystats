
init:
	pip install -r requirements.txt

test:
	python setup.py test

doc:	html readme

html:
	$(MAKE) -C docs $@

readme:
	cat ./initial.rst ./docs/source/intro.rst ./docs/source/quickstart.rst > README.rst

package:
	python setup.py sdist

publish:
	python setup.py sdist upload

.PHONY: init test html doc readme package publish
