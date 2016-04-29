import pyshark
import argparse

parser = argparse.ArgumentParser(description='Outputs stats')
parser.add_argument("pcap", metavar="PCAP", type=str, help="filepath for pcap")

args = parser.parse_args()

cap = pyshark.FileCapture(args.pcap)

sd = {}
d = dict()
i = 0

def convo(pkt):
	try:
		#protocol = pkt.transport_layer
		highest = pkt.highest_layer
		src_addr = pkt.ip.src
		src_port = pkt[pkt.transport_layer].srcport
		dst_addr = pkt.ip.dst
		dst_port = pkt[pkt.transport_layer].dstport
		if (highest, src_addr, src_port, dst_addr, dst_port) not in sd:
			sd[(highest, src_addr, src_port, dst_addr, dst_port)] = 1
		else:
			sd[(highest, src_addr, src_port, dst_addr, dst_port)] += 1
	except AttributeError as e:
		#ignore packets that aren't TCP/UDP or IPv4
		pass

for p in cap:
	i += 1
	if p.highest_layer not in d:
		d[p.highest_layer] = 1
	else:
		d[p.highest_layer] += 1
	convo(p)
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

print "\n\n(highest, src_addr, src_port, dst_addr, dst_port): count"
for p in sd:
	print "(" + str(p[0]) + ", " + str(p[1]) + ", " + str(p[2]) + ", " + str(p[3]) + ", " + str(p[4]) + "): " +str(sd[p])
