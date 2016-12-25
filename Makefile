
init:
	pip install -r requirements.txt

test:
	python setup.py test

html:
	$(MAKE) -C docs $@

package:
	python setup.py sdist

publish:
	python setup.py sdist upload

.PHONY: init test html
