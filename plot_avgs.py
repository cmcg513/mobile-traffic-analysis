import plotly
import plotly.graph_objs as go
import argparse

parser = argparse.ArgumentParser(description='Outputs barchart')
parser.add_argument("stats", metavar="STATS", type=str, nargs="+", help="filepath(s) for stats output")
parser.add_argument("-i", "--ignore_protoc", type=str, nargs="+", help="protoc(s) to exclude from graph")
parser.add_argument("-o", "--output_filename", type=str, help="filename of output html file")

