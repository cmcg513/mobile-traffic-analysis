import plotly
import plotly.graph_objs as go
import argparse

parser = argparse.ArgumentParser(description='Outputs barchart')
parser.add_argument("stats", metavar="STATS", type=str, nargs="+", help="filepath(s) for stats output")
parser.add_argument("-i", "--ignore_protoc", type=str, nargs="+", help="protoc(s) to exclude from graph")
parser.add_argument("-o", "--output_filename", type=str, help="filename of output html file")


args = parser.parse_args()

if args.ignore_protoc:
	ignore_list = list(args.ignore_protoc)
	for i in range(len(ignore_list)):
		ignore_list[i] = ignore_list[i].upper()
else:
	ignore_list = []


stat_dict = dict()
all_protocs = set()

for stat_filename in args.stats:
	ifl = open(stat_filename, 'r')
	stat_dict[stat_filename] = dict()

	for line in ifl:
		proto, avg = line.strip().split("|")

		if proto in ignore_list:
			continue

		stat_dict[stat_filename][proto] = avg
		all_protocs.add(proto)

data = []
all_protocs = sorted(all_protocs)

for stat_filename in stat_dict:
	x = []
	y = []
	for protoc in all_protocs:
		x.append(protoc)
		if protoc in stat_dict[stat_filename]:
			y.append(stat_dict[stat_filename][protoc])
		else:
			y.append(0)

	data.append(go.Bar(x=x, y=y, name=stat_filename))

layout = go.Layout(barmode='group')
fig = go.Figure(data=data, layout=layout)

if args.output_filename:
	plotly.offline.plot(fig, filename=args.output_filename)
else:
	plotly.offline.plot(fig)












