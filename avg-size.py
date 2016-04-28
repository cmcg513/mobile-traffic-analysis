import pyshark

cap = pyshark.FileCapture("../casey_cap_1.pcap")
ofl = open("cc1.txt", 'w')


dproto = {}
dprotoSize = {}
i = 0

for p in cap:
	i += 1
	if i % 10000 == 0:
		print i

	try:
		key = p.highest_layer

		if key not in dproto:
			dproto[key] = 1
			dprotoSize[key] = int(p.length)
		else:
			dproto[key] += 1
			dprotoSize[key] += int(p.length)

	except AttributeError as e:
		continue


for k in dproto:
	print k
	print "avg size: ", dprotoSize[k] / dproto[k]
	ofl.write(str(k) + "|");
	ofl.write(str(dprotoSize[k] / dproto[k]));
	ofl.write("\n");

