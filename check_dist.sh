set -e
#rmvirtualenv temp
#mkvirtualenv temp
bash create_dist.sh
pip install .
cd ~/Downloads
rm -Rf py_mock_data_test_dist
mkdir py_mock_data_test_dist
cd py_mock_data_test_dist
cp ~/projects/py-data-mock/requirements_test_dist.txt .
pip install -r requirements_test_dist.txt
cp -R $PROJECTS_DIR/py-data-mock/unittests .
bash unittests/test_all.sh
