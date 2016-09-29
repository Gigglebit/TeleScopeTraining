from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaIoBaseDownload
import os
import io
import sys
import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument('file_id')

# try:
# 	import argparse
# 	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
# 	flags = None




SCOPES = 'https://www.googleapis.com/auth/drive.file'+' '+'https://www.googleapis.com/auth/drive.readonly'
CLIENT_SECRET = 'client_secret.json'
# flags = tools.argparser.parse_args(args=[])
store = file.Storage('storage.json')
credz = store.get()
if not credz or credz.invalid:
	flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
	credz = tools.run_flow(flow, store, flags) \
			if flags else tools.run(flow, store)


DRIVE = build('drive', 'v3', http=credz.authorize(Http()))
#SERVICE = build(API, VERSION, developerKey = API_KEY)
# files= SERVICE.files().list().execute().get('items',[])
# for f in files:
# 	print (f['title'], f['mimeType'])

# FILES = (
# 	('Win10_1607_English_x64.iso', False)
# )https://drive.google.com/open?id=0BxtzJzlgRwjrVFJ3bFVTNlEtaUU

# res, data = DRIVE._http.request(res[])

#file_id = '0B9ejphBUrJL_U1gyanNzNTJrQUE'

file_id = sys.argv[1]
#file_id = '0BxtzJzlgRwjrQ1pIU3ZMWTUyODg'
request = DRIVE.files().get_media(fileId=file_id)
fh = io.BytesIO()
downloader = MediaIoBaseDownload(fh, request)
done = False
while done is False:
    status, done = downloader.next_chunk()
    print ("Download %d%%." % int(status.progress() * 100))

#https://drive.google.com/open?id=0B9ejphBUrJL_bzNNcDg1a1hTQm90NnEweV9UTjl6NHRBQ2pV
#https://drive.google.com/open?id=0B_gon-PYFdP_cFJ5UmJXNGpvVDQ
#https://drive.google.com/open?id=0B9ejphBUrJL_dHUxWlIzSWpkNndIQ1Zicm5sQVVpMGVKSVN3
#https://drive.google.com/open?id=0BxtzJzlgRwjrQ1pIU3ZMWTUyODg
#https://drive.google.com/open?id=0B9ejphBUrJL_WjdfOGc2blF0czQ
#https://drive.google.com/file/d/0B9ejphBUrJL_cWpjSUM0OWtxbElPU2pIU0x0Yk5yd1FDWGdF/view?usp=sharing
#https://drive.google.com/file/d/0B9ejphBUrJL_WjdfOGc2blF0czQ/view?usp=sharing
#https://drive.google.com/open?id=0B9ejphBUrJL_bi0yZDRVUzJYUU0
#https://drive.google.com/file/d/0B9ejphBUrJL_bi0yZDRVUzJYUU0/view?usp=sharing
#https://drive.google.com/file/d/0B9ejphBUrJL_cWpjSUM0OWtxbElPU2pIU0x0Yk5yd1FDWGdF/view?usp=sharing
#https://drive.google.com/open?id=0BxtzJzlgRwjrQ1pIU3ZMWTUyODg
#https://drive.google.com/open?id=0B9ejphBUrJL_U1gyanNzNTJrQUE