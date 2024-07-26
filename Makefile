worker:
	celery -A yolodocs.tasks worker -l INFO --autoscale 8,2
