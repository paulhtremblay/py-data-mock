#gcloud builds submit --region=us-west1 --tag gcr.io/paul-henry-tremblay/some-image .
source conf.sh
gcloud builds submit --region=us-west1 --config cloudbuild.yaml . \
	--substitutions=_PYPI_USERNAME=$_PYPI_USERNAME,_PYPI_PASSWORD=$_PYPI_PASSWORD
