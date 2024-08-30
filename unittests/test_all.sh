set -e

python -m unittest unittests/test_client.py\
	unittests/test_psycopg2.py \
	unittests/test_requests.py 
