DOCKER="docker"
IMAGE_NAME="kiansheik/timucua"
TAG_NAME="production"

REPOSITORY=""
FULL_IMAGE_NAME=${IMAGE_NAME}:${TAG_NAME}

lint:
	zsh -c 'cd timucua; python3.11 setup.py sdist bdist_wheel;'
	echo 'kiansheik.io' > CNAME
	black .

push:
	make lint
	git add .
	git commit
	git push origin HEAD

gen_data:
	python3.11 ankigen_timucua.py
# 	python3 timucua/tests/context.py
# 	python3.11 pdf_extract.py