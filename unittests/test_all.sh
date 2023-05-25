set -e

python -m unittest unittests/test_client.py\
	unittests/test_table.py \
	unittests/test_provider.py \
    unittests/test_unittest_ex.py \
    unittests/test_from_bucket.py \
