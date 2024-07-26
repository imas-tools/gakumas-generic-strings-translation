update:
	cd gakumas-generic-source-strings && git fetch && git checkout origin/main

gen-todo:
	python scripts/gen.py

arrange:
	python scripts/arrange.py

apply:
	python scripts/apply.py

pretranslate:
	python scripts/pretranslate.py

normalize:
	python scripts/normalize.py
