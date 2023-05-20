set -e
#twine upload --repository testpypi dist/*
twine upload -r pypi dist/*
