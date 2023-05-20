set -e
rm -Rf dist
rm -Rf build

python setup.py check
python setup.py sdist
python setup.py bdist_wheel --universal
