Welcome to the PDF Annotation API Project!
===============================================

This is the PDF Annotation Service for PDF annotation tool that was written in React. 
It is responsible for managing documents, annotations and users info/roles,
as well as serves as a bridge to call Nominatim's location API service. 
We manage the data using AWS RDS (prefer to use MySQL or Postgres).
It exposes standard APIs that allow the frontEnd application manage a 
the relevant data and functionalities.  


----------  


Responsibilities of this service
-------------

This service will manage the following:  
 - Users and access control on the application.
 - Uploaded PDF documents.  
 - Annotations on the uploaded PDF documents.  
 - Named Entities that should be used to extract annotations on Spacy.      
  
  

Get code running
-------------

Make sure you have python3 installed on the machine.


> **Steps:**
> - Set environment variables as stipulated in table below in the section **```Environment Variables```**
> - ```pipenv install```
> > - ```pipenv run api```
> - Check base at http://{{service_base_url}}

----------


Extra
--------------------
> **Tip:** You can change the application's configurable items 
in the ```config/settings.py``` file at the project root alongside 
other configurable items. 


### Routes


Item     					  | Value                                     | Description
----------------------------- | ----------------------------------------- | ----------------------
Base     				      | /                                         | The base endpoint
Health     				      | /health                                   | check the health of this service
Setup Application        	  | /setup-application                        | setup default manager account
Login        	              | /login                                    | log into application (JWT)
All Users        	          | /users                                    | all users
All Documents        	      | /documents                                | all documents
All Annotations        	      | /annotations                              | all annotations
All Annotations on Document   | /documents/:documentId/annotations        | all annotations on a document
Spacy Named Entities          | /named-entities                           | spacy named entities

  
  
  
API documentation
-------------------  
  
  
See API documentation in Postman collection.
  
    
  


### Environment Variables to set


Item     					| Value
--------------------------- | ---------------------------
ENVIRONMENT     			| (development, production, staging)
API_HOST     			    | Host for api to run on
API_PORT     			    | Port for app to run on
AWS_RDS_CONNECTION_URI 	    | Database full connection uri(this takes priority if not empty)
AWS_RDS_HOST 			    | Database host
AWS_RDS_PORT      	        | Database Port Number
AWS_RDS_USER      	        | Database Username
AWS_RDS_PASSWORD      	    | Database Password for the user
AWS_RDS_DATABASE_NAME      	| The name of the Database within AWS RDS
AWS_RDS_LOG_LEVEL 	        | String(error, warning, info, debug, trace)
LOCATION_LOOKUP_URL 	    | The endpoint to call to lookup longitude and Latitude (should be nominatim.org service)
LOG_LEVEL  		            | String(error, warn, info, verbose, debug, silly)
LOG_ENABLE_CONSOLE          | Boolean(true/false)
