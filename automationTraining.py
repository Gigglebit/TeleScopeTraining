import sys
import os
#import httplib
import json
import requests
#import webbrowser
import subprocess as sp
import time

# read from 129.94.5.44:8080/stats/controller
# r = requests.get('https://github.com/timeline.json')
# r.json()

#fo = open("out_summary.txt", "w")
#fo.write('')
#fo.close()

#,"https://www.youtube.com/watch?v=O9F5Yk1WOKo","https://www.youtube.com/watch?v=Iwt08oPbX5A","https://www.youtube.com/watch?v=Eho8HDtkCiU","https://www.youtube.com/watch?v=k2GnFFajzTA","https://www.youtube.com/watch?v=H9vevyszht4","https://www.youtube.com/watch?v=xS4RPj7IPGM","https://www.youtube.com/watch?v=qdKqn32kUKU","https://www.youtube.com/watch?v=mRq5nzWbZNg","https://www.youtube.com/watch?v=LGlipVxtvbM","https://www.youtube.com/watch?v=KUiDyQxHHk0","https://www.youtube.com/watch?v=50GBci6ToVA&list=PLKkDjgBOPjWHvsizaCkXLN9HDtl3kU_Yw"
#360 ,"https://www.youtube.com/watch?v=ETvHZ8ITSdQ&index=2&list=PLm6qoFmp6K51Kne3BQo8_aN0s54y2jGfx","https://www.youtube.com/watch?v=YAWy4LjS4Fc","https://www.youtube.com/watch?v=ckDHQQ7PXCo","https://www.youtube.com/watch?v=tM6_n9VwLQM","https://www.youtube.com/watch?v=iDfsGX5pCHk&list=PLU8wpH_LfhmvMokgsfQtiHNsP96bU7cnr&index=9","https://www.youtube.com/watch?v=9ngmwMVDIx8&list=PLU8wpH_LfhmvMokgsfQtiHNsP96bU7cnr&index=12","https://www.youtube.com/watch?v=H2Jc1wHlhEU&list=PLU8wpH_LfhmvMokgsfQtiHNsP96bU7cnr&index=29"

YoutubeList=["https://www.youtube.com/watch?v=WQ2c9DB3EnU","https://www.youtube.com/watch?v=OvSG1EimSIs","https://www.youtube.com/watch?v=O9F5Yk1WOKo","https://www.youtube.com/watch?v=Iwt08oPbX5A","https://www.youtube.com/watch?v=Eho8HDtkCiU","https://www.youtube.com/watch?v=k2GnFFajzTA","https://www.youtube.com/watch?v=H9vevyszht4","https://www.youtube.com/watch?v=xS4RPj7IPGM","https://www.youtube.com/watch?v=qdKqn32kUKU","https://www.youtube.com/watch?v=mRq5nzWbZNg","https://www.youtube.com/watch?v=LGlipVxtvbM","https://www.youtube.com/watch?v=KUiDyQxHHk0","https://www.youtube.com/watch?v=50GBci6ToVA&list=PLKkDjgBOPjWHvsizaCkXLN9HDtl3kU_Yw"]

TszList=["https://www.youtube.com/watch?v=Qd6EaMd37jA&index=1&list=PLm6qoFmp6K51Kne3BQo8_aN0s54y2jGfx","https://www.youtube.com/watch?v=ETvHZ8ITSdQ&index=2&list=PLm6qoFmp6K51Kne3BQo8_aN0s54y2jGfx","https://www.youtube.com/watch?v=YAWy4LjS4Fc","https://www.youtube.com/watch?v=ckDHQQ7PXCo","https://www.youtube.com/watch?v=tM6_n9VwLQM","https://www.youtube.com/watch?v=iDfsGX5pCHk&list=PLU8wpH_LfhmvMokgsfQtiHNsP96bU7cnr&index=9","https://www.youtube.com/watch?v=9ngmwMVDIx8&list=PLU8wpH_LfhmvMokgsfQtiHNsP96bU7cnr&index=12","https://www.youtube.com/watch?v=H2Jc1wHlhEU&list=PLU8wpH_LfhmvMokgsfQtiHNsP96bU7cnr&index=29"]

inspectedIpList=list()

def loopThroughVideoList(videoList,tag):
	for video in videoList:
		################## open firefox ###################	
		#webbrowser.get('firefox').open_new_tab(video)
		child = sp.Popen("firefox %s" % video, shell=True)
		time.sleep(30)

		######## get the srcIp and dstPort ####################
		srcIp=''
		dstPort=70000 # in order to find the smallest port, set the initial value bigger than any possible port number

		i=0 ### loop parameter
		while srcIp == '' and i < 10:
			r = requests.get(url='http://129.94.5.44:8080/stats/controller')
			jsonObject = r.json()

			flows = jsonObject.get('flows')
			for flowDict in flows:
				if flowDict['isVideo'] == True:
					tempsrcIp = flowDict['srcIp']
					if tempsrcIp not in inspectedIpList:
						srcIp=tempsrcIp
					#print(flowDict)

			stats = jsonObject.get('stats')
			for sd in stats:
				if sd['sourceIP'] == srcIp and sd['tp_dst'] <= dstPort :
					dstPort = sd['tp_dst']
					#print(sd)

			i=i+1
			time.sleep(5)

		if srcIp == '' or dstPort == 70000:
			print("can't get srcIp or dstPort")
			#sys.exit(0)
			continue
	
		inspectedIpList.append(srcIp)
		print(srcIp,dstPort)

		################## execute the query_on_ryu.py to get the real time summary info ################
		for x in range(7):
			executeQueryStr = "python query_on_ryu.py {} {} {}".format(srcIp,dstPort,tag)
			os.system(executeQueryStr)
			time.sleep(10)
		
		################ close firefox #######################
		child.kill()
		child.terminate()

		################ wait for the auto erasing to erase the current flow info #########################
		#time.sleep(30)


loopThroughVideoList(YoutubeList,1)
loopThroughVideoList(TszList,2)

#call_training_program_string = "python sixFeatureTeleSVMImpl.py out_summary.txt"
#os.system(call_training_program_string)

os.system("sudo shutdown -h now")




















