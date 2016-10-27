from time import gmtime, strftime
import subprocess
from datetime import datetime,timedelta
from threading import Timer

from influxdb import InfluxDBClient
import csv,datetime

from time import mktime
import json
import requests
import time
import subprocess as sp
import dateutil.parser as dp
import sys,os
import numpy as np
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


def dump_l3_flows(desctag):
	users = []
	servers = []
	flows = []

	# providers = ["uniwide"]
	# applications = ["youtube"]
	provider = "uniwide"
	application = "youtube"
	dst_ip = '129.94.5.92'
	src_ip = fetchSrcIp(dst_ip)


	time_frame = 5 #5mins resolution
	DURATION_OFFSET = 16
	DURATION_LIMIT = 129


	timeFrom = "now() - {}h - {}m - {}s".format("0","0",str(DURATION_LIMIT+DURATION_OFFSET))
	timeTo = "now() - {}h - {}m".format("0","0","0")
	limit = str(20000)

	query_string = "SELECT * FROM l3Stat WHERE application = \'" + application +"\'  AND provider = \'" + provider+ "\' AND src_ip = \'" + src_ip + "\' AND dst_ip = \'" + dst_ip +"\'  AND time >= "+ timeFrom +" AND time < " + timeTo + " LIMIT "+ limit+ " ;"
	print query_string 
	duration = 0
	terminating_counter = 0
	while (duration < DURATION_LIMIT):
		print duration
		print "Waiting for another 16 seconds"
		time.sleep(DURATION_OFFSET)
		result = client.query(query_string)
		if "series" not in result.raw:
			return -1
		values = result.raw["series"][0]["values"]
		columns = result.raw["series"][0]["columns"]
		index_duration = columns.index("duration")
		duration = values[-1][index_duration]

		if (terminating_counter > 10):
			return -1
		terminating_counter = terminating_counter + 1

	
	#print result
	if "series" not in result.raw:
		return -1
	#print result
	values = result.raw["series"][0]["values"]
	#print len(values)
	columns = result.raw["series"][0]["columns"]
	#print columns
	#print result.raw["series"][0]["name"]

	index_stat_id = columns.index("stat_id")
	index_byte_count = columns.index("byte_count")
	index_dst_ip = columns.index("dst_ip")
	index_src_ip = columns.index("src_ip")
	index_time = columns.index("time")
	index_duration = columns.index("duration")
	index_provider = columns.index("provider")
	index_flow_count = columns.index("flow_count")

	#process data 
	flowlist = {}
	src_ip_list = []
	dst_ip_list = []
	previous_duration = -1
	rawlist = []
	for entry in values:
		#print entry
		if entry[index_duration] < DURATION_LIMIT and entry[index_duration]!=previous_duration:			
			if entry[index_src_ip]==src_ip and entry[index_dst_ip]==dst_ip: 
				#print '----matched srcIP and dstIP----'
				t = entry[index_time]
				parsed_t = dp.parse(t)
				t_in_seconds = parsed_t.strftime('%s')
				row = t_in_seconds+','+str(entry[index_byte_count])+','+str(entry[index_stat_id])+','+str(entry[index_duration])+','+entry[index_src_ip]+','+entry[index_dst_ip]+','+str(entry[index_flow_count])+'\n'
				# if entry missing:

				while (entry[index_duration] - previous_duration) > 1:
					previous_duration = previous_duration + 1
					row = t_in_seconds+','+str(entry[index_byte_count])+','+str(entry[index_stat_id])+','+str(previous_duration)+','+entry[index_src_ip]+','+entry[index_dst_ip]+','+str(entry[index_flow_count])+'\n'
					rawlist.append(row)

				rawlist.append(row)
				#print "rawlist:"+row
				previous_duration = entry[index_duration]
	
	with open('out_detail_l3db_all.txt', 'a') as f:
		# f.write ('time,bytes,pkts,duration,srcIp,srcPort,dstIp,dstPort\n')
		f.write ('------------- entry src:%s,entry dst: %s,desctag: %s ----------------\n' % (src_ip,dst_ip,desctag))
		#print rawlist
		for entry in rawlist:
			f.write(entry)		

	with open('out_detail_l3db.txt', 'w') as f:
		# f.write ('time,bytes,pkts,duration,srcIp,srcPort,dstIp,dstPort\n')
		f.write ('------------- entry src:%s,entry dst: %s ----------------\n' % (src_ip,dst_ip))
		#print rawlist
		for entry in rawlist:
			f.write(entry)
	print ("END script")
	return 0

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
	with open('out_detail_l3db.txt', 'r') as the_file:
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
	sum_flow_count = 0.0
	rate_bytes = 0
	rate_pkts = 0
	i = 0
	duration = 0
	for entry in content:
		sum_flow_count = sum_flow_count + float(entry.split(',')[-1])
		if prev_entry!="":
			#print entry.split(',')[0]

			delta_t = int(entry.split(',')[0])-int(init_t)

			delta_bytes = int(entry.split(',')[1])-int(prev_entry.split(',')[1])

			delta_t_list.append(delta_t)
			delta_bytes_list.append(delta_bytes)
			
			sum_bytes = sum_bytes + delta_bytes
			sum_t = delta_t
			# print delta_bytes
			# print i
			# print delta_t
			if i % 2 == 0:
				delta_bytes_mod2_list.append(delta_bytes_list[i-1]+delta_bytes_list[i-2])
			if i % 4 == 0:
#				print delta_bytes_mod2_list
				delta_bytes_mod4_list.append(delta_bytes_mod2_list[i/2-1]+delta_bytes_mod2_list[i/2-2])
			if i % 8 == 0:
				delta_bytes_mod8_list.append(delta_bytes_mod4_list[i/4-1]+delta_bytes_mod4_list[i/4-2])
			if i % 16 == 0:
				delta_bytes_mod16_list.append(delta_bytes_mod8_list[i/8-1]+delta_bytes_mod8_list[i/8-2])
		duration = int(entry.split(',')[3])
		i = i + 1 		
		prev_entry = entry
	if sum_t!=0:
		rate_bytes = sum_bytes/sum_t
		# rate_pkts = sum_pkts/sum_t
	print "----- The rate of this flow (Bytes/s)------"
	mu = rate_bytes
	print mu
	# print "----- The rate of this flow (Packet/s)------"
	# print rate_pkts	
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
	f1.append(sum_flow_count/(end-start))
	
	print '------mu---::',(mu/1000)
	print 'tag:',tag
	print f1
	#print f2
	with open('out_summary_l3.txt', 'a') as f:
		f.write(','.join(str(e) for e in f1))
		f.write('\n')
	# if tag ==1 and (mu/1000) > 50:
	# 	with open('out_summary_l3.txt', 'a') as f:
	# 		f.write(','.join(str(e) for e in f1))
	# 		f.write('\n')
 #             #f.write(','.join(str(e) for e in f2))
	# elif tag ==2 and (mu/1000) >187:
	# 	with open('out_summary_l3.txt', 'a') as f:
	# 		f.write(','.join(str(e) for e in f1))
	# 		f.write('\n')
	# elif tag ==3 and (mu/1000) >750:
	# 	with open('out_summary_l3.txt', 'a') as f:
	# 		f.write(','.join(str(e) for e in f1))
	# 		f.write('\n')


def fetchSrcIp(myIp):
		srcIp =''
		i = 0 ### loop parameter
		
		while srcIp == '' and i < 10:
			try:
			    r = requests.get(url='http://129.94.5.44:8080/stats/controller')
			except requests.exceptions.ConnectionError:
			    r.status_code = "Connection refused"
			    break
			
			jsonObject = r.json()
			flows = jsonObject.get('flows')
			for flowDict in flows:
				if flowDict['isVideo'] == True: 
					if flowDict['dstIp'] == myIp and flowDict['duration']<30:
						srcIp = flowDict['srcIp']
						return srcIp
			print(srcIp)
			i=i+1
			time.sleep(5)
		return srcIp

def loopThroughVideoList(videoList):
	youtube_prefix = "https://www.youtube.com/watch?v="
	
	j = 0 

	YTtag=0
	for video in videoList:
		video = youtube_prefix + video
		################## open firefox ###################	
		#webbrowser.get('firefox').open_new_tab(video)
		child = sp.Popen("firefox %s" % video, shell=True)
		time.sleep(20)

		if j<5:
			tag=1
		elif j>=5 and j<10:
			tag=2
		elif j>=10 and j<=15:
			tag=3
		else:
			print "tag error"

		j = j + 1
		tempYTtag = str(YTtag)
		retval = dump_l3_flows(tempYTtag)
		if retval == -1:
			print("can't get flow stats")
			os.system("wmctrl -a firefox; xdotool key Ctrl+w; wmctrl -r firefox -b add,shaded")
			#sys.exit(0)
			continue
	
		

		if (retval!=-1):
			print '---extract features---'
			extract_better_features(1, 18, tag,'YT'+tempYTtag)
			extract_better_features(1, 34, tag,'YT'+tempYTtag)
			extract_better_features(1, 50, tag,'YT'+tempYTtag)
			extract_better_features(1, 66, tag,'YT'+tempYTtag)
			extract_better_features(17, 82, tag,'YT'+tempYTtag)
			extract_better_features(33, 98, tag,'YT'+tempYTtag)
			extract_better_features(50, 114, tag,'YT'+tempYTtag)
			extract_better_features(66, 130, tag,'YT'+tempYTtag)

		print '----------------video--------------------------'
		#if x == 6:
		os.system("wmctrl -a firefox; xdotool key Ctrl+w; wmctrl -r firefox -b add,shaded")
		time.sleep(10)
		

		YTtag+=1
		time.sleep(40)
if __name__ == "__main__":
	# tag = 1
	# tempYTtag = "0"
	# extract_better_features(1, 17, tag,'YT'+tempYTtag)	
	content = []
	with open('3607201440pids', 'r') as f:
		content = f.readlines()

	#tempCount = 0

	while 1:
		loopThroughVideoList(content)
		#tempCount += 1
	# dump_l3_flows()
