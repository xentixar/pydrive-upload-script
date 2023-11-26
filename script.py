from pydrive.drive import GoogleDrive 
from pydrive.auth import GoogleAuth 

# For using listdir() 
import os 

folder_name = {"Folder 1","Folder 2","Folder 3"}

# Below code does the authentication 
# part of the code 
gauth = GoogleAuth() 

# Creates local webserver and auto 
# handles authentication. 
gauth.LocalWebserverAuth()	 
drive = GoogleDrive(gauth) 
	
# Fetch the existing folder - Main Folder
existing_folder_name = 'Main Folder'
existing_folder_query = f"title = '{existing_folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
existing_folders = drive.ListFile({'q': existing_folder_query}).GetList()

if len(existing_folders) == 0:
	print(f"Error: Folder '{existing_folder_name}' not found.")
	exit()

# Get the id of the existing folder -  Main Folder
existing_folder_id = existing_folders[0]['id']

# Create a new Test Folder inside the Main Folder
folder_metadata = {'title': 'Test Folder', 'mimeType': 'application/vnd.google-apps.folder','parents':[{'id':existing_folder_id}]}
folder_1 = drive.CreateFile(folder_metadata)
folder_1.Upload()

# Loop through each folder_name
for i in folder_name:
	# Create a folder with the required folder_name
	folder_metadata = {'title': i, 'mimeType': 'application/vnd.google-apps.folder', 'parents':[{'id':folder_1['id']}]}
	folder = drive.CreateFile(folder_metadata)
	folder.Upload()

	# Create a Sub Folder inside the above created folder
	subfolder_metadata = {'title': 'Sub Folder', 'mimeType': 'application/vnd.google-apps.folder', 'parents': [{'id': folder['id']}]}
	subfolder = drive.CreateFile(subfolder_metadata)
	subfolder.Upload()

	# replace the value of this variable 
	# with the absolute path of the directory 
	path = r"D:/Test Folder"

	# iterating thought all the files/folder 
	# of the desired directory 
	for x in os.listdir(path): 
		f = drive.CreateFile({'title': x,'parents': [{'id': folder['id']}]}) 
		f.SetContentFile(os.path.join(path, x)) 
		f.Upload() 

		# Due to a known bug in pydrive if we 
		# don't empty the variable used to 
		# upload the files to Google Drive the 
		# file stays open in memory and causes a 
		# memory leak, therefore preventing its 
		# deletion 
		f = None

