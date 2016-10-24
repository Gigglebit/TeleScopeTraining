from influxdb import InfluxDBClient
import dateutil.parser as dp
import sys
import numpy as np
import datetime

import time

#configurable DB
INFLUXDB_DB = "flowBucket"
INFLUXDB_HOST = "129.94.5.44"
INFLUXDB_PORT = 8086
INFLUXDB_USER = ""
INFLUXDB_PASS = ""

client = InfluxDBClient(
         host=INFLUXDB_HOST, port=INFLUXDB_PORT,
         username=INFLUXDB_USER, password=INFLUXDB_PASS,
         database=INFLUXDB_DB, timeout=10)



dbs = client.get_list_database()
# #print dbs


ret_policies = client.get_list_retention_policies(INFLUXDB_DB)
#print ret_policies
def retrieve_flow_entries_from_influxdb(src_ip,dst_ip,dst_port):
	#src_ip = sys.argv[1]

	""" Test 1"""
	timeFrom = "now() - 5m"
	timeTo = "now()"
	limit = str(1000)
	duration = 0
	terminating_counter = 0
	while (duration < 128):
		result = client.query("SELECT * FROM flowStat WHERE time > "+ timeFrom +" AND time < " + timeTo + " AND src_ip = \'" + src_ip + "\' ORDER BY time ASC LIMIT "+ limit+ " ;")
		values = result.raw["series"][0]["values"]
		columns = result.raw["series"][0]["columns"]
		index_duration = columns.index("duration")
		duration = values[-1][index_duration]
		if (terminating_counter > 10):
			return -1
		terminating_counter = terminating_counter + 1

		time.sleep(16)
#	result = client.query("SELECT * FROM flowStat WHERE time > "+ timeFrom +" AND time < " + timeTo + " ORDER BY time ASC LIMIT "+ limit+ " ;")

#	print (result)
	values = result.raw["series"][0]["values"]
	#print (len(values))
	columns = result.raw["series"][0]["columns"]
	#print (columns)
	#print (result.raw["series"][0]["name"])

	index_cookie = columns.index("flow_id")
	index_byte_count = columns.index("byte_count")
	index_packet_count = columns.index("packet_count")
	index_dst_port = columns.index("dst_port")
	index_dst_ip = columns.index("dst_ip")
	index_src_port = columns.index("src_port")
	index_src_ip = columns.index("src_ip")
	index_time = columns.index("time")
	index_duration = columns.index("duration")
	rawlist=[]
	#process data 
	flowlist = {}
	#dst_ip = '129.94.5.92'
	#dst_port = sys.argv[2]
	dst_port_list = []
	i = 0
	j = 0
	port_diff = 20
	previous_duration = 0
	

	for entry in values:
		print entry
		if entry[index_duration] <= 128:
			if entry[index_dst_ip]==dst_ip and entry[index_dst_port]==dst_port:
				row = ''
			#print entry[0]

				t = entry[index_time]
				byte_count = entry[index_byte_count]
				packet_count = entry[index_packet_count]
				
	#			print len(values)
				for j in range(len(values[i+1:])):
	#				print values[j]				
					if values[j][index_time]==t:
						if int(values[j][index_dst_port])<int(dst_port)+port_diff and int(values[j][index_dst_port])>int(dst_port)-port_diff:
							byte_count=byte_count+values[j][index_byte_count]
							packet_count=packet_count+values[j][index_packet_count]
							break
					else:
						break	
				parsed_t = dp.parse(t)
				t_in_seconds = parsed_t.strftime('%s')
				row = t_in_seconds+','+str(entry[index_byte_count])+','+str(entry[index_packet_count])+','+str(entry[index_duration])+','+entry[index_src_ip]+','+entry[index_src_port]+','+entry[index_dst_ip]+','+entry[index_dst_port]+'\n'
				# if entry missing:
				while (entry[index_duration] - previous_duration) > 1:
					rawlist.append(row)
					previous_duration = previous_duration + 1
					

				rawlist.append(row)
				previous_duration = entry[index_duration]
			#cookie =  entry[index_cookie]
			#byte_count = entry[index_byte_count]
			#time = entry[index_time]
			if entry[index_dst_ip]+':'+entry[index_dst_port] not in dst_port_list:
				dst_port_list.append(entry[index_dst_ip]+':'+entry[index_dst_port])
			#if cookie not in flowlist:
				#flowlist[cookie] = {}
				#flowlist[cookie]["time"] = []
				#flowlist[cookie]["byte_count"] = []
				#flowlist[cookie]["dst_ip"] = entry[index_dst_ip]
				#flowlist[cookie]["src_ip"] = entry[index_src_ip]
				#flowlist[cookie]["byte_count"].append(byte_count)
				#flowlist[cookie]["time"].append(time)
			i = i + 1
	print 'Available dst_port numbers are'
	print dst_port_list

		#else:
		#	flowlist[cookie]["byte_count"].append(byte_count)
		#	flowlist[cookie]["time"].append(time)
	#print rawlist
	# with open('out.txt', 'w') as f:
	# 	print ('time,bytes,pkts,duration,srcIp,srcPort,dstIp,dstPort\n')
	# 	for entry in rawlist:
	# 		f.write(entry)
	with open('out_detail.txt', 'w') as f:
		# f.write ('time,bytes,pkts,duration,srcIp,srcPort,dstIp,dstPort\n')
		f.write ('------------- entry src:%s,entry dst: %s:%s ----------------' % src_ip,dst_ip,dstPort)
		for entry in rawlist:
			f.write(entry)
#	f.close()

	#print (flowlist)


	""" Test 2"""


	#reset database 
	#client.drop_database(INFLUXDB_DB)
	#client.create_database(INFLUXDB_DB)

	print ("END script")
	return 1

def calculate_sigma(B,j,mu):
	#print "--------method 1 mod %s--------" %(j)
	m1 = np.sqrt(np.sum(np.power((B/j-mu),2))/(B.size*mu))
	#print m1
	#print "--------method 2 mod %s --------" %(j)
	m2 = np.sqrt(np.sum(np.power((B-mu),2))/(B.size*j))
	#print m2
	return m1, m2

def extract_better_features(start, end, tag, desctag):
	raw_content = []
	content = []
	with open('out_detail.txt', 'r') as the_file:
		raw_content = the_file.readlines()

	content = raw_content[start: end]
	if (len(content))==0:
		return 
	prev_entry = "" 
	delta_t_list = []
	delta_bytes = 0
	delta_pkts = 0
	delta_bytes_list = []
	delta_bytes_mod2_list = []
	delta_bytes_mod4_list = []
	delta_bytes_mod8_list = []
	delta_bytes_mod16_list = []
	delta_pkts_list = []
	init_t = content[0].split(',')[0]
	sum_t = 0
	sum_bytes = 0
	sum_pkts = 0
	rate_bytes = 0
	rate_pkts = 0
	i = 0
	duration = 0
	for entry in content:
		if prev_entry!="":
			#print entry.split(',')[0]

			delta_t = int(entry.split(',')[0])-int(init_t)
			while delta_t - i > 0:
				delta_t_list.append(i)
				delta_bytes_list.append(delta_bytes)
				delta_pkts_list.append(delta_pkts)
				sum_pkts = sum_pkts + delta_pkts
				sum_bytes = sum_bytes + delta_bytes
	                        if i % 2 == 0:
        	                        delta_bytes_mod2_list.append(delta_bytes_list[i-1]+delta_bytes_list[i-2])
                	        if i % 4 == 0:
#                               print delta_bytes_mod2_list
                        	        delta_bytes_mod4_list.append(delta_bytes_mod2_list[i/2-1]+delta_bytes_mod2_list[i/2-2])
                        	if i % 8 == 0:
                                	delta_bytes_mod8_list.append(delta_bytes_mod4_list[i/4-1]+delta_bytes_mod4_list[i/4-2])
                        	if i % 16 == 0:
                                	delta_bytes_mod16_list.append(delta_bytes_mod8_list[i/8-1]+delta_bytes_mod8_list[i/8-2])
				i = i + 1

			delta_bytes = int(entry.split(',')[1])-int(prev_entry.split(',')[1])
			delta_pkts = int(entry.split(',')[2])-int(prev_entry.split(',')[2])
			delta_t_list.append(delta_t)
			delta_bytes_list.append(delta_bytes)
			delta_pkts_list.append(delta_pkts)
			sum_pkts = sum_pkts + delta_pkts
			sum_bytes = sum_bytes + delta_bytes
			sum_t = delta_t

			if delta_t % 2 == 0:
				delta_bytes_mod2_list.append(delta_bytes_list[i-1]+delta_bytes_list[i-2])
			if delta_t % 4 == 0:
#				print delta_bytes_mod2_list
				delta_bytes_mod4_list.append(delta_bytes_mod2_list[delta_t/2-1]+delta_bytes_mod2_list[delta_t/2-2])
			if delta_t % 8 == 0:
				delta_bytes_mod8_list.append(delta_bytes_mod4_list[delta_t/4-1]+delta_bytes_mod4_list[delta_t/4-2])
			if delta_t % 16 == 0:
				delta_bytes_mod16_list.append(delta_bytes_mod8_list[delta_t/8-1]+delta_bytes_mod8_list[delta_t/8-2])
		duration = int(entry.split(',')[3])
		i = i + 1 		
		prev_entry = entry
	if sum_t!=0:
		rate_bytes = sum_bytes/sum_t
		rate_pkts = sum_pkts/sum_t
	print "----- The rate of this flow (Bytes/s)------"
	mu = rate_bytes
	print mu
	print "----- The rate of this flow (Packet/s)------"
	print rate_pkts	
	m1 = 0.0
	m2 = 0.0
	f1=[]
	f2=[]
	f1.append(mu)
	f2.append(mu)
	m1,m2 = calculate_sigma(np.array(delta_bytes_list),1,mu)
	f1.append(m1)
	f2.append(m2)
	#print delta_bytes_list
	m1,m2 = calculate_sigma(np.array(delta_bytes_mod2_list),2,mu)
	f1.append(m1)
	f2.append(m2)
	#print delta_bytes_mod2_list
	m1,m2 = calculate_sigma(np.array(delta_bytes_mod4_list),4,mu)
	f1.append(m1)
	f2.append(m2)
	#print delta_bytes_mod4_list
	m1,m2 = calculate_sigma(np.array(delta_bytes_mod8_list),8,mu)
	f1.append(m1)
	f2.append(m2)	
	#print delta_bytes_mod8_list
	m1,m2 = calculate_sigma(np.array(delta_bytes_mod16_list),16,mu)
	f1.append(m1)
	f2.append(m2)
	f1.append(duration)
	f2.append(duration)
	f1.append(tag)#YouTube 1 / YouTube360 2
	f2.append(tag)
	#print delta_bytes_mod16_list 
	f1.append(desctag)
	f1.append(datetime.datetime.now())
	tag = tag
	print '------mu---::',(mu/1000)
	print 'tag:',tag
	print f1
	#print f2
	if tag == '1' and (mu/1000) > 50:
		with open('out_summary_mov.txt', 'a') as f:
			f.write(','.join(str(e) for e in f1))
			f.write('\n')
             #f.write(','.join(str(e) for e in f2))
	elif tag =='2' and (mu/1000) >187:
		with open('out_summary_mov.txt', 'a') as f:
			f.write(','.join(str(e) for e in f1))
			f.write('\n')
	elif tag =='3' and (mu/1000) >750:
		with open('out_summary_mov.txt', 'a') as f:
			f.write(','.join(str(e) for e in f1))
			f.write('\n')




#retrieve_flow_entries_from_influxdb()
#extract_features()














import os
#import httplib
import json
import requests
#import webbrowser
import subprocess as sp

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
# with open('youtubeAllResolutionids', 'r') as f:
# 	youtube_content = f.readlines()

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

		#tag=42

		##change to ,tag 1 stands for 360p, tag 2 720p, tag 3 1440ps

		if j<5:
			tag=1
		elif j>=5 and j<10:
			tag=2

		elif j>=10 and j<=15:
			tag=3
		else:
			print "tag error"


		# elif j>=10:
		# 	tag=3
		#tag=4d 

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
		dstIp = '129.94.5.92'
		################## execute the query_on_ryu.py to get the real time summary info ################
		#for x in range(7):
		tempYTtag = str(YTtag)
		retval = retrieve_flow_entries_from_influxdb(srcIp, dstIp, dstPort)
		if (retval!=-1):
			extract_better_features(1, 16, tag,'YT'+tempYTtag)
			extract_better_features(1, 32, tag,'YT'+tempYTtag)
			extract_better_features(1, 48, tag,'YT'+tempYTtag)
			extract_better_features(1, 64, tag,'YT'+tempYTtag)
			extract_better_features(17, 80, tag,'YT'+tempYTtag)
			extract_better_features(33, 96, tag,'YT'+tempYTtag)
			extract_better_features(49, 112, tag,'YT'+tempYTtag)
			extract_better_features(65, 128, tag,'YT'+tempYTtag)
		#executeQueryStr = "python query_on_ryu.py {} {} {} {}".format(srcIp,dstPort,tag,'YT'+tempYTtag)
		#os.system(executeQueryStr)
		print '------The Above calculation is based on this Ip and Port-----'
		print(srcIp,dstPort)
		# if tag == 1:
		# 	print '---------------YouTube 1080p---------------'
		# else:
		# 	print '---------------360 Degree 1080s------------'
		print '----------------video--------------------------'
		#if x == 6:
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


# comment this part use only 3607201440ids
# lenYT = len(youtube_content)
# len360 = len(youtube360_content)


lenYT = len(youtube_content)
# len360 = len(youtube360_content)


# if len360 == lenYT:
# 	for i in range(len360):
# 		content.append(youtube_content[i])
# 		content.append(youtube360_content[i])


with open('3607201440pids', 'r') as f:
#with open('youtube1080ids', 'r') as f:
	content = f.readlines()


#for i in range(lenYT):
#	content.append(youtube_content[i])
		
#print content 
# i%2 == 0 tag 1; i%2 == 1 tag 2 

tempCount = 0

while tempCount < 10:
	loopThroughVideoList(content)
	tempCount += 1
# loopThroughVideoList(TszList,2)

	#gDriveDownloadFunction()
	#gDriveDownloadFunction()
	#gDriveDownloadFunction()
	#gDriveDownloadFunction()
	#gDriveDownloadFunction()

	# gDriveDownloadFunction()
	# gDriveDownloadFunction()
	# gDriveDownloadFunction()
	# gDriveDownloadFunction()
	# gDriveDownloadFunction()



#call_training_program_string = "python sixFeatureTeleSVMImpl.py out_summary.txt"
#os.system(call_training_program_string)

#os.system("sudo shutdown -h now")






