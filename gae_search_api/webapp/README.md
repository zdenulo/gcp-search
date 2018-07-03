#Setting up GAE app and deployment

This assumes that you have installed GAE SDK (Cloud SDK)

Before deployment you need to install libraries in requirement.txt file

``pip install -r requirements.txt -t lib``

To upload application, you need to execute command (after you authenticate and set correct project with gcloud) 

``gcloud app deploy . --promote``

