# Repository Description
This repository is a simple guide to demonstrate how to use Google Drive API in Python

# Introduction
Google Drive is a cloud storage platform that is extensively used worldwide for storing files online and accessing them from anywhere and on any device. Google provides a RESTful API that can be used to manage these files programmatically. This guide will walk you through the process of using the Google Drive API in Python to interact with files stored on Google Drive.

Python's google-auth, google-auth-oauthlib, google-auth-httplib2, and google-api-python-client packages offer functionalities for authenticating and interacting with the Google Drive API.

# Setting up your Google Drive API
1. Go to the Google Cloud Console (console.cloud.google.com).
2. Click "Select a project" > "NEW PROJECT", and then create a new project.
3. On the dashboard of your new project, go to "Library" > "Drive API" and enable the Drive API for your project.
4. Go to "Credentials" on the sidebar, and click "Create Credentials" > "OAuth client ID". Fill in the required fields, select "Other", and then create and download the JSON file.
5. Rename the downloaded JSON file to credentials.json and place it in your project folder.

