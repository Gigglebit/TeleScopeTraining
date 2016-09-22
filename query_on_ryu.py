from influxdb import InfluxDBClient
import dateutil.parser as dp
import sys
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



dbs = client.get_list_database()
# #print dbs


ret_policies = client.get_list_retention_policies(INFLUXDB_DB)
#print ret_policies
def retrieve_flow_entries_from_influxdb():
	src_ip = sys.argv[1]

	""" Test 1"""
	timeFrom = "now() - 5m"
	timeTo = "now()"
	limit = str(1000)

	result = client.query("SELECT * FROM flowStat WHERE time > "+ timeFrom +" AND time < " + timeTo + " AND src_ip = \'" + src_ip + "\' ORDER BY time ASC LIMIT "+ limit+ " ;")
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
	dst_ip = '129.94.5.92'
	dst_port = sys.argv[2]
	dst_port_list = []
	i = 0
	j = 0
	port_diff = 20
	for entry in values:
		print entry
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
			rawlist.append(row)

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
	with open('out.txt', 'w') as f:
		print ('time,bytes,pkts,duration,srcIp,srcPort,dstIp,dstPort\n')
		for entry in rawlist:
			f.write(entry)
	with open('out_all.txt', 'a') as f:
		f.write ('time,bytes,pkts,duration,srcIp,srcPort,dstIp,dstPort\n')
		for entry in rawlist:
			f.write(entry)
#	f.close()

	#print (flowlist)


	""" Test 2"""


	#reset database 
	#client.drop_database(INFLUXDB_DB)
	#client.create_database(INFLUXDB_DB)

	print ("END script")

def calculate_sigma(B,j,mu):
	#print "--------method 1 mod %s--------" %(j)
	m1 = np.sqrt(np.sum(np.power((B/j-mu),2))/B.size)
	#print m1
	#print "--------method 2 mod %s --------" %(j)
	m2 = np.sqrt(np.sum(np.power((B-mu),2))/(B.size*j))
	#print m2
	return m1, m2

def extract_features():
	content = []
	with open('out.txt', 'r') as the_file:
		content = the_file.readlines()
	if (len(content))==0:
		return 
	prev_entry = "" 
	delta_t_list = []
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

			delta_bytes = int(entry.split(',')[1])-int(prev_entry.split(',')[1])
			delta_pkts = int(entry.split(',')[2])-int(prev_entry.split(',')[2])
			delta_t_list.append(delta_t)
			delta_bytes_list.append(delta_bytes)
			delta_pkts_list.append(delta_pkts)
			sum_pkts = sum_pkts + delta_pkts
			sum_bytes = sum_bytes + delta_bytes
			sum_t = delta_t
			#print delta_t_list
			#print delta_bytes_list
			# print i
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
	f1.append(sys.argv[3])#YouTube 1 / YouTube360 2
	f2.append(sys.argv[3])
	#print delta_bytes_mod16_list 
	print f1
	print f2
        with open('out_summary.txt', 'a') as f:
             f.write(','.join(str(e) for e in f1))
	     f.write('\n')
             #f.write(','.join(str(e) for e in f2))
retrieve_flow_entries_from_influxdb()
extract_features()
