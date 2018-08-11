#Setting Autocomplete with Google Cloud Spanner and Google App Engine Flex

##Creating Spanner instance
In console.cloud.google.com on the left top menu, go to Spanner section, click on 'Create new instance'. 
I called instance 'eshopxx', based on variable in file search.spanner_search.py.
  
##Creating Service Account
in Cloud Console again, when you go to IAM -> Service Accounts. You need to click on Create, give it some name and select Role.
You need to go to Spanner part and set Role to be Spanner Admin (the highest role). Also check option to furnish (download)
Json file with secret (you can download only once that file). For sake of simplicity / compatibility rename it to 'service_account.json'

##Local setup
I'm using here Google App Engine Flexible since provided library doesn't work on Standard (I would need to use REST API)
You need to install requirements under virtualenv (for Python 3)

```pip install -r requirements.txt```

It's normal Flask application, so locally you can run it with:


```
export FLASK_APP=main.py
python -m flask run
```

##Uploading data
in file 'upload_products.py' you need to set again url for your app and execute file with python to upload data.
It's printing every respone (200, ok) and also number of so far deployed products

##Deploying
since this is Google App Engine Flexible, there is a little bit different approach for deployment

```gcloud app deploy app.yaml --verbosity=debug  --promote --version=spanner``` 

It basically creates Docker image under the hood and deploys it.
I'm not sure if something else needs to be enabled (since lots of things are changing, it's hard to catch up everything)...
flags mean following:
--verbosity - just to have some idea what's going during deployment
--promote - it promotes this version to handle traffic on main url i.e. http://<project-id>.appspot.com/
otherwise second working url is also http://<version>.<project-id>.appspot.com
--version - name of version. if ommited, version name will be timestamp or something like that.
 
##Working with app
in main.py you have all routes and description of what they do so it should be self explaining

##Important!!!
Google App Engine Flex(ible) has different properties than Standard. One of them is that one instance is always alive, 
so when you are done with this, delete GAE instance and also Spanner, since it costs ~0.9$ per one hour :)

Hopefully I didn't forgot anything