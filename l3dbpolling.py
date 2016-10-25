from time import gmtime, strftime
import subprocess
from datetime import datetime,timedelta
from threading import Timer

from influxdb import InfluxDBClient
import csv,datetime

from time import mktime

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


def dump_l3_flows():
	users = []
	servers = []
	flows = []

	#providers = ["dorm","uniwide"]
	providers = ["uniwide"]
	application = ["google"]
	#applications = ["facebook","google","iView","netflix"]
	dst_ip = '129.94.5.85'
	for provider in providers:
		for application in applications:
			for num in range(0,1): #2 iteration

				time_frame = 5 #5mins resolution

				offset_from_min = (num+1)*time_frame 
				offset_to_min = num*time_frame

				timeFrom = "now() - {}h - {}m".format("0",str(offset_from_min))
				timeTo = "now() - {}h - {}m".format("0",str(offset_to_min))
				limit = str(20000)

				query_string = "SELECT * FROM l3Stat WHERE application = \'" + application +"\'  AND provider = \'" + provider+ " AND dst_ip = \'" + dst_ip +"\'  AND time >= "+ timeFrom +" AND time < " + timeTo + " LIMIT "+ limit+ " ;"
				print query_string 

				result = client.query(query_string)

				if "series" not in result.raw:
					continue

				#print result
				values = result.raw["series"][0]["values"]
				print len(values)
				columns = result.raw["series"][0]["columns"]
				print columns
				print result.raw["series"][0]["name"]

				index_stat_id = columns.index("stat_id")
				index_byte_count = columns.index("byte_count")
				index_dst_ip = columns.index("dst_ip")
				index_src_ip = columns.index("src_ip")
				index_time = columns.index("time")
				index_duration = columns.index("duration")
				index_provider = columns.index("provider")

				#process data 
				flowlist = {}
				src_ip_list = []
				dst_ip_list = []

				# filename = strftime("%Y%m%d", gmtime())+ '_l3Stat_' + provider+'_' + application +'.csv'

				# with open(filename, 'a') as f:
				# 	writer = csv.writer(f)
				# 	values  = sorted(values, key=lambda k: k[index_time],reverse=True)

				# 	for entry in values:

				# 		stat_id =  entry[index_stat_id]
				# 		byte_count = entry[index_byte_count]
				# 		time = entry[index_time]

				# 		src_ip = entry[index_src_ip]
				# 		dst_ip = entry[index_dst_ip]
				# 		duration = entry[index_duration]

				# 		try:

				# 			dt = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")

				# 			ms_since_epoch = int( (mktime(dt.timetuple()) + dt.microsecond/1000000.0) * 1000) 

				# 			fields=[str(ms_since_epoch),str(stat_id),str(duration),str(byte_count),str(src_ip),str(dst_ip)]
				# 			writer.writerow(fields)
					
				# 		except:
				# 			pass

dump_l3_flows()
# def dump_group_stats():
# 	users = []
# 	servers = []
# 	flows = []

# 	for num in range(0,12*24):

# 		time_frame = 5

# 		offset_from_min = (num+1)*time_frame 
# 		offset_to_min = num*time_frame

# 		timeFrom = "now() - {}h - {}m".format("0",str(offset_from_min))
# 		timeTo = "now() - {}h - {}m".format("0",str(offset_to_min))
# 		limit = str(20000)

# 		query_string = "SELECT * FROM groupStat WHERE time > "+ timeFrom +" AND time < " + timeTo + " LIMIT "+ limit+ " ;"
# 		print query_string 

# 		result = client.query(query_string)

# 		if "series" not in result.raw:
# 			continue

# 		#print result
# 		values = result.raw["series"][0]["values"]
# 		print len(values)
# 		columns = result.raw["series"][0]["columns"]
# 		print columns
# 		print result.raw["series"][0]["name"]

# 		index_time = columns.index("time")
# 		index_byte_count = columns.index("byte_count")
# 		index_ref_count = columns.index("ref_count")
# 		index_group_id = columns.index("group_id")
# 		index_rate = columns.index("rate")


# 		filename = strftime("%Y%m%d", gmtime()) + '_group.csv'
# 		with open(filename, 'a') as f:
# 			writer = csv.writer(f)

# 			values  = sorted(values, key=lambda k: k[index_time],reverse=True)

# 			for entry in values:
# 				byte_count = entry[index_byte_count]
# 				time = entry[index_time]
# 				group_id = entry[index_group_id]
# 				ref_count = entry[index_ref_count]
# 				rate =  entry[index_rate]

# 				try:

# 					dt = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")

# 					ms_since_epoch = int( (mktime(dt.timetuple()) + dt.microsecond/1000000.0) * 1000) 

# 					fields=[str(ms_since_epoch),str(byte_count),str(ref_count),str(rate),str(group_id)]
# 					writer.writerow(fields)
				
# 				except:
# 					pass

				


# 			f.close()


# def truncate_log():
# 	bashCommand = "cp /var/www/seer/current/log/seerevent.log "+ " /var/www/seer/current/log/"+strftime("%Y%m%d%H%M%S", gmtime())+"_seerevent.log"
# 	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
# 	output = process.communicate()[0]
# 	print output


# 	bashCommand = "truncate -s0 /var/www/seer/current/log/seerevent.log"
# 	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
# 	output = process.communicate()[0]
# 	print output



# def looper_fn():

# 	dump_l3_flows();
# 	dump_group_stats();
# 	set_timer()


# def set_timer():

# 	nextDay = datetime.datetime.now() + timedelta(days=1)

# 	#sydney gmt +11
# 	dateString = nextDay.strftime('%d-%m-%Y') + " 6-01-00"
# 	print dateString
# 	newDate = nextDay.strptime(dateString,'%d-%m-%Y %H-%M-%S')
# 	delay = (newDate -  datetime.datetime.now()).total_seconds()
# 	print delay
	
# 	t = Timer(delay, looper_fn)
# 	t.start()

# set_timer()

