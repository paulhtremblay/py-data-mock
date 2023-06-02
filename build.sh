gcloud builds submit --region=us-west1 --config cloudbuild.yaml . \
	--substitutions=_PYPI_USERNAME=$_PYPI_USERNAME,_PYPI_PASSWORD=$_PYPI_PASSWORD
