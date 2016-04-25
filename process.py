import pyshark

cap = pyshark.FileCapture('MS-Capture-1.pcap')

# s = set()
d = dict()
i = 0

for p in cap:
	i += 1
	if p.highest_layer not in d:
		d[p.highest_layer] = 0
	else:
		d[p.highest_layer] += 1
	if i % 10000 == 0:
		print i
	# s.add(p.highest_layer)
	# if p.highest_layer in ['BOOTP','BROWSER','DATA','DATA-TEXT-LINES','DB-LSP-DISC']:
	# 	print str(i) + " --- " + p.highest_layer

print "Total packets: " + str(i)
print "Total counts: "
protocs = sorted(d.keys())
for protoc in protocs:
	print "\t" + protoc + ": " + str(d[protoc])
print "Percentages: "
for protoc in protocs:
	print "\t" + protoc + ": " + str(float(d[protoc])/float(i)*100)