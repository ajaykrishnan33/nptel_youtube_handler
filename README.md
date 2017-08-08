# Youtube Handler Scripts for NPTEL

# Installation instructions
	1. pip install --upgrade google-api-python-client

	2. Go to https://console.developers.google.com/flows/enableapi?apiid=youtube

	3. Login using your Google ID.

	4. Click Continue, then "Go to credentials".

	5. On the Add credentials to your project page, click the Cancel button.

	6. At the top of the page, select the OAuth consent screen tab. Select an Email address, enter a Product name if not already set, and click the Save button.

	7. Select the Credentials tab, click the Create credentials button and select OAuth client ID.

	8. Select the application type Other, enter the name "YouTube Data API Quickstart", and click the Create button.

	9. Click OK to dismiss the resulting dialog.

	10.Click the download button to the right of the client ID.

	11.Move this file to this directory and rename it client_secret.json

# Running instructions

	For downloading all srts corresponding to a particular GMail ID:

		$ python download_srts.py

		This will open a Google sign-in page in the browser. Sign-in with the correct GMail ID for which the subtitles need to be downloaded. 
		The download will now begin.

	For uploading all srts corresponding to a particular GMail ID:

		(This will also work for updating existing subtitles.)

		$ python get_videos_list.py

		This will open a Google sign-in page in the browser. Sign-in with the correct GMail ID for which the subtitles need to be downloaded. 
		This will get a list of videos corresponding to the signed-in GMail ID which will be stored in videos.csv .

		Edit videos.csv and enter the path of the subtitle file next to the corresponding video title by changing it from "None". All entries need not be updated, ie. if subtitle file is not available for some video, then leave it as "None". Existing subtitles will be automatically updated. 

		$ python upload_subtitles.py --folder=<complete-path-to-transcripts-folder>

		This will open a Google sign-in page in the browser. Sign-in with the correct GMail ID for which the subtitles need to be downloaded. 
		This will upload the subtitles mentioned in videos.csv to YouTube.

