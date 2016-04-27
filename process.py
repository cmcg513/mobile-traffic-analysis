import pyshark
import argparse

parser = argparse.ArgumentParser(description='Outputs stats')
parser.add_argument("pcap", metavar="PCAP", type=str, help="filepath for pcap")

args = parser.parse_args()

cap = pyshark.FileCapture(args.pcap)

d = dict()
i = 0

for p in cap:
	i += 1
	if p.highest_layer not in d:
		d[p.highest_layer] = 1
	else:
		d[p.highest_layer] += 1
	if i % 10000 == 0:
		print i

print "Total packets: " + str(i)
print "Total counts: "
protocs = sorted(d.keys())
for protoc in protocs:
	print "\t" + protoc + ": " + str(d[protoc])
print "Percentages: "
for protoc in protocs:
	print "\t" + protoc + ": " + str(float(d[protoc])/float(i)*100)