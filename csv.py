import pyshark
import argparse

parser = argparse.ArgumentParser(description='Outputs stats')
parser.add_argument("pcap", metavar="PCAP", type=str, help="filepath for pcap")

args = parser.parse_args()

cap = pyshark.FileCapture(args.pcap)

ip = {}
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
			ip[(highest, src_addr, dst_addr)] = 1
		else:
			sd[(highest, src_addr, src_port, dst_addr, dst_port)] += 1
			ip[(highest, src_addr, dst_addr)] += 1
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

print "Total packets," + str(i)

protocs = sorted(d.keys())
print "\n,Protocol,Count"
for protoc in protocs:
	print "," + protoc + "," + str(d[protoc])

print "\n,Protocol,Percent"
for protoc in protocs:
	print "," + protoc + "," + str(float(d[protoc])/float(i)*100)

ip_keys = []
for key in ip:
	ip_keys.append(key)
ip_keys = sorted(ip_keys)
print "\n\n,Protocol,Source IP,Destination IP,Count"
for key in ip_keys:
	print "," + key[0] + "," + key[1] + "," + key[2] + "," + str(ip[key])

keys = []
for key in sd:
	keys.append(key)
keys = sorted(keys)
print "\n\n,Protocol,Source IP,Source Port,Destination IP,Destination Port,Count"
for key in keys:
	print "," + key[0] + "," + key[1] + "," + key[2] + "," + key[3] + "," + key[4] + "," + str(sd[key])

