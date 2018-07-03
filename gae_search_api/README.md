
# SETUP
works under Python 2.7 since Google App Engine Standard doesn't supports 3.x    
to install necessary third party libraries (Flask web framework)
```pip install -r requirements.txt```

# DEPLOY Google App Engine
```gcloud app deploy -v search --promote```  
search is name of the version (instead of default timestamp)  
--promote is flag to automatically use this as default version



