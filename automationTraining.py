import sys
import os
#import httplib
import json
import requests
#import webbrowser
import subprocess as sp
import time
import signal
# read from 129.94.5.44:8080/stats/controller
# r = requests.get('https://github.com/timeline.json')
# r.json()

#fo = open("out_summary.txt", "w")
#fo.write('')
#fo.close()
youtube_content = []
youtube360_content = []
gDriveID = []
#,"https://www.youtube.com/watch?v=O9F5Yk1WOKo","https://www.youtube.com/watch?v=Iwt08oPbX5A","https://www.youtube.com/watch?v=Eho8HDtkCiU","https://www.youtube.com/watch?v=k2GnFFajzTA","https://www.youtube.com/watch?v=H9vevyszht4","https://www.youtube.com/watch?v=xS4RPj7IPGM","https://www.youtube.com/watch?v=qdKqn32kUKU","https://www.youtube.com/watch?v=mRq5nzWbZNg","https://www.youtube.com/watch?v=LGlipVxtvbM","https://www.youtube.com/watch?v=KUiDyQxHHk0","https://www.youtube.com/watch?v=50GBci6ToVA&list=PLKkDjgBOPjWHvsizaCkXLN9HDtl3kU_Yw"
#360 ,"https://www.youtube.com/watch?v=ETvHZ8ITSdQ&index=2&list=PLm6qoFmp6K51Kne3BQo8_aN0s54y2jGfx","https://www.youtube.com/watch?v=YAWy4LjS4Fc","https://www.youtube.com/watch?v=ckDHQQ7PXCo","https://www.youtube.com/watch?v=tM6_n9VwLQM","https://www.youtube.com/watch?v=iDfsGX5pCHk&list=PLU8wpH_LfhmvMokgsfQtiHNsP96bU7cnr&index=9","https://www.youtube.com/watch?v=9ngmwMVDIx8&list=PLU8wpH_LfhmvMokgsfQtiHNsP96bU7cnr&index=12","https://www.youtube.com/watch?v=H2Jc1wHlhEU&list=PLU8wpH_LfhmvMokgsfQtiHNsP96bU7cnr&index=29"
#with open('youtube1080ids', 'r') as f:
with open('youtubeAllResolutionids', 'r') as f:
	youtube_content = f.readlines()
# with open('youtube360degree', 'r') as f:
# #with open('temp360Test', 'r') as f:
# 	youtube360_content = f.readlines()	
youtube_prefix = "https://www.youtube.com/watch?v="

with open('gDriveFileID','r') as f:
	gDriveID=f.readlines() 


# YoutubeList=["https://www.youtube.com/watch?v=WQ2c9DB3EnU","https://www.youtube.com/watch?v=OvSG1EimSIs","https://www.youtube.com/watch?v=O9F5Yk1WOKo","https://www.youtube.com/watch?v=Iwt08oPbX5A","https://www.youtube.com/watch?v=Eho8HDtkCiU","https://www.youtube.com/watch?v=k2GnFFajzTA","https://www.youtube.com/watch?v=H9vevyszht4","https://www.youtube.com/watch?v=xS4RPj7IPGM","https://www.youtube.com/watch?v=qdKqn32kUKU","https://www.youtube.com/watch?v=mRq5nzWbZNg","https://www.youtube.com/watch?v=LGlipVxtvbM","https://www.youtube.com/watch?v=KUiDyQxHHk0","https://www.youtube.com/watch?v=50GBci6ToVA&list=PLKkDjgBOPjWHvsizaCkXLN9HDtl3kU_Yw"]

# TszList=["https://www.youtube.com/watch?v=Qd6EaMd37jA&index=1&list=PLm6qoFmp6K51Kne3BQo8_aN0s54y2jGfx","https://www.youtube.com/watch?v=ETvHZ8ITSdQ&index=2&list=PLm6qoFmp6K51Kne3BQo8_aN0s54y2jGfx","https://www.youtube.com/watch?v=YAWy4LjS4Fc","https://www.youtube.com/watch?v=ckDHQQ7PXCo","https://www.youtube.com/watch?v=tM6_n9VwLQM","https://www.youtube.com/watch?v=iDfsGX5pCHk&list=PLU8wpH_LfhmvMokgsfQtiHNsP96bU7cnr&index=9","https://www.youtube.com/watch?v=9ngmwMVDIx8&list=PLU8wpH_LfhmvMokgsfQtiHNsP96bU7cnr&index=12","https://www.youtube.com/watch?v=H2Jc1wHlhEU&list=PLU8wpH_LfhmvMokgsfQtiHNsP96bU7cnr&index=29"]

inspectedIpList=list()

def loopThroughVideoList(videoList):
	myIp = u'129.94.5.92'
	j = 0 

	YTtag=0
	for video in videoList:
		video = youtube_prefix + video
		################## open firefox ###################	
		#webbrowser.get('firefox').open_new_tab(video)
		child = sp.Popen("firefox %s" % video, shell=True)
		time.sleep(20)

		######## get the srcIp and dstPort ####################
		srcIp=''
		dstPort=70000 # in order to find the smallest port, set the initial value bigger than any possible port number
		print(srcIp,dstPort)
		# if j % 2 == 0:
		# 	tag = 1
		# else:
		# 	tag = 2
<<<<<<< HEAD
		#tag=42

		##change to ,tag 1 stands for 360p, tag 2 720p, tag 3 1440ps
=======
>>>>>>> 51d6bac47bf835ad0c084e2942b7306c0ce5f1df
		if j<5:
			tag=1
		elif j>=5 and j<10:
			tag=2
<<<<<<< HEAD
		elif j>=10 and j<=15:
			tag=3
		else:
			print "tag error"

=======
		elif j>=10:
			tag=3
		#tag=4
>>>>>>> 51d6bac47bf835ad0c084e2942b7306c0ce5f1df
		i = 0 ### loop parameter
		j = j + 1

		while srcIp == '' and i < 10:
			try:
			    r = requests.get(url='http://129.94.5.44:8080/stats/controller')
			except requests.exceptions.ConnectionError:
			    r.status_code = "Connection refused"
			    break
			
			jsonObject = r.json()

			flows = jsonObject.get('flows')
			for flowDict in flows:
				#print flowDict
				if flowDict['isVideo'] == True: 
					# print flowDict['dstIp']
					# print myIp
					# print flowDict['dstIp'] == myIp
					if flowDict['dstIp'] == myIp and flowDict['duration']<30:

						srcIp = flowDict['srcIp']
						#if tempsrcIp not in inspectedIpList:
						# 	srcIp=tempsrcIp
						#print(flowDict)

						stats = jsonObject.get('stats')
						potentialVideos = []
						for sd in stats:
							if sd['sourceIP'] == srcIp:
								potentialVideos.append(sd)
								#dstPort = sd['tp_dst']
						print "--------------potentialVideos-----------"	
						maxbytes = 0						
						for vd in potentialVideos:
							print vd
							if vd['byte'] > maxbytes:
								maxbytes = vd['byte']
								dstPort = vd['tp_dst']

						print dstPort
					#print(sd)
			print(srcIp,dstPort)
			i=i+1
			time.sleep(5)

		if srcIp == '' or dstPort == 70000:
			print("can't get srcIp or dstPort")
			os.system("wmctrl -a firefox; xdotool key Ctrl+w; wmctrl -r firefox -b add,shaded")
			#sys.exit(0)
			continue
	
		# inspectedIpList.append(srcIp)

		################## execute the query_on_ryu.py to get the real time summary info ################
		for x in range(7):
			tempYTtag = str(YTtag)+str(x)
			executeQueryStr = "python query_on_ryu.py {} {} {} {}".format(srcIp,dstPort,tag,'YT'+tempYTtag)
			os.system(executeQueryStr)
			print '------The Above calculation is based on this Ip and Port-----'
			print(srcIp,dstPort)
			# if tag == 1:
			# 	print '---------------YouTube 1080p---------------'
			# else:
			# 	print '---------------360 Degree 1080s------------'
			print '----------------video--------------------------'
			if x == 6:
				os.system("wmctrl -a firefox; xdotool key Ctrl+w; wmctrl -r firefox -b add,shaded")
			time.sleep(10)
		
		################ close firefox #######################
		# child.kill()
		# child.terminate()
		#val = 
		#os.system("wmctrl -a firefox; xdotool key Ctrl+w; wmctrl -r firefox -b add,shaded")
		YTtag+=1
		time.sleep(30)
		
		#os.system("killall -9 firefox")
		#print val
		################ wait for the auto erasing to erase the current flow info #########################
		

def gDriveDownloadFunction():
	myIp = u'129.94.5.92'
	NonYTtag=0
	for id in gDriveID:
		##start downloading###
		exegDriveDownload = "python gDriveDownload.py "+id
		#os.system(exegDriveDownload)
		p = sp.Popen(exegDriveDownload,shell = True,preexec_fn=os.setsid)

		#p = sp.Popen(['python','gDriveDownload.py',id])

		######## get the srcIp and dstPort ####################
		srcIp=''
		dstPort=70000 # in order to find the smallest port, set the initial value bigger than any possible port number
		i=0

		while srcIp == '' and i < 10:
			try:
			    r = requests.get(url='http://129.94.5.44:8080/stats/controller')
			except requests.exceptions.ConnectionError:
			    r.status_code = "Connection refused"
			    break
			
			jsonObject = r.json()
			flows = jsonObject.get('flows')
			for flowDict in flows:
				#print flowDict
				if flowDict['isVideo'] == True: 
					# print flowDict['dstIp']
					# print myIp
					# print flowDict['dstIp'] == myIp
					if flowDict['dstIp'] == myIp and flowDict['duration']<30:

						srcIp = flowDict['srcIp']
						#if tempsrcIp not in inspectedIpList:
						# 	srcIp=tempsrcIp
						#print(flowDict)

						stats = jsonObject.get('stats')
						potentialVideos = []
						for sd in stats:
							if sd['sourceIP'] == srcIp:
								potentialVideos.append(sd)
								#dstPort = sd['tp_dst']
						print "--------------potentialVideos-----------"	
						maxbytes = 0						
						for vd in potentialVideos:
							print vd
							if vd['byte'] > maxbytes:
								maxbytes = vd['byte']
								dstPort = vd['tp_dst']
						print dstPort
					#print(sd)
			print(srcIp,dstPort)
			i=i+1
			time.sleep(5)

		if srcIp == '' or dstPort == 70000:
			print("can't get srcIp or dstPort")
			os.killpg(os.getpgid(p.pid), signal.SIGTERM)
			p.kill()
			p.terminate()
			#sys.exit(0)
			continue

		### wait for data to synchronize###
		time.sleep(10)
		################## execute the query_on_ryu.py to get the real time summary info ################
		for x in range(10):
			tempNonYTtag=str(NonYTtag)+str(x)
			executeQueryStr = "python query_on_ryu.py {} {} {} {}".format(srcIp,dstPort,3,'NonYT'+tempNonYTtag)
			os.system(executeQueryStr)
			#print '------The Above calculation is based on this Ip and Port-----'
			print(srcIp,dstPort)
			
			if x == 9:
				# os.system("wmctrl -a firefox; xdotool key Ctrl+w; wmctrl -r firefox -b add,shaded")
				os.killpg(os.getpgid(p.pid), signal.SIGTERM)
				p.kill()
				p.terminate()

			time.sleep(10)
		
		################ close firefox #######################
		# child.kill()
		# child.terminate()
		p.kill()
		p.terminate()
		
		#val = 
		#os.system("wmctrl -a firefox; xdotool key Ctrl+w; wmctrl -r firefox -b add,shaded")
		## wait 30s , the SDN switch will remove the flow entry which haven't been activated for 30s
		NonYTtag+=1
		time.sleep(30)


content = []
<<<<<<< HEAD

# comment this part use only 3607201440ids
# lenYT = len(youtube_content)
# len360 = len(youtube360_content)

=======
lenYT = len(youtube_content)
# len360 = len(youtube360_content)

>>>>>>> 51d6bac47bf835ad0c084e2942b7306c0ce5f1df
# if len360 == lenYT:
# 	for i in range(len360):
# 		content.append(youtube_content[i])
# 		content.append(youtube360_content[i])
<<<<<<< HEAD

with open('3607201440pids', 'r') as f:
#with open('youtube1080ids', 'r') as f:
	content = f.readlines()
=======
>>>>>>> 51d6bac47bf835ad0c084e2942b7306c0ce5f1df

#for i in range(lenYT):
#	content.append(youtube_content[i])
		
#print content 
# i%2 == 0 tag 1; i%2 == 1 tag 2 

tempCount = 0

while tempCount < 10:
	loopThroughVideoList(content)
	tempCount += 1
# loopThroughVideoList(TszList,2)
<<<<<<< HEAD
	#gDriveDownloadFunction()
	#gDriveDownloadFunction()
	#gDriveDownloadFunction()
	#gDriveDownloadFunction()
	#gDriveDownloadFunction()
=======
	# gDriveDownloadFunction()
	# gDriveDownloadFunction()
	# gDriveDownloadFunction()
	# gDriveDownloadFunction()
	# gDriveDownloadFunction()
>>>>>>> 51d6bac47bf835ad0c084e2942b7306c0ce5f1df


#call_training_program_string = "python sixFeatureTeleSVMImpl.py out_summary.txt"
#os.system(call_training_program_string)

#os.system("sudo shutdown -h now")



















