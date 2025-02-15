#!/usr/bin/env python

#Luis Zaman
#5/9/12

from numpy import loadtxt, transpose
from matplotlib import pyplot
import argparse


#build the parser object for us
parser = argparse.ArgumentParser(description="Plots one or more columns from a typical Avida file")

#file to parse
parser.add_argument('--data_file', type=argparse.FileType('r'), help="the filename containing space delimited values to be plotted", required=True)
parser.add_argument('--x_column', type=int, help="Column to be used as the X values for the plot", required=True, nargs=1)

#label for the axes
parser.add_argument('--x_label', type=str, help="x-axis label, if you need spaces you can quote the string", required=False, default="x-axis", nargs=1)
parser.add_argument('--y_label', type=str, help="y-axis label, if you need spaces you can quote the string", required=False, default="y-axis", nargs=1)

#which columns to plot
parser.add_argument('--columns', type=int, help="Column to be used as the Y values for the plot", required=True, nargs="+")
#what to label those columns
parser.add_argument('--column_labels', type=str, help="Space delimited labels to be used for individual columns, if spaces are desired within labels the labels can be quoted", required=False, nargs="+", default=None)

#optional log axes 
parser.add_argument('--log_x', help="Graph the x-axis on a log scale", required=False, default=False, action='store_true')
parser.add_argument('--log_y', help="Graph the y-axis on a log scale", required=False, default=False, action='store_true')
parser.add_argument('--grid', help="Use an axes grid", required=False, default=False, action='store_true')

#save figure
parser.add_argument('--out_file', help="Save the figure to this file, using the extension format", required=False, default=None)

args = parser.parse_args()


#load in the data, using the x-column and the columns to plot using numpy's handy loadtxt function
data_matrix = loadtxt(args.data_file, usecols=args.x_column + args.columns, unpack=True)

#plot the data we need, where x=the first row of the matrix, and the rest of the lines are
#the the rest of columns of the matrix.
pyplot.plot(data_matrix[0], transpose(data_matrix[1:]))

#handle the toggles
if args.log_y:
    pyplot.gca().set_yscale("log")
if args.log_x:
    pyplot.gca().set_xscale("log")
if args.grid:
    pyplot.grid()
    
#check if we need to label them, and if we do make sure we have the right number of labels
if args.column_labels:
    assert len(args.columns) == len(args.column_labels), 'Number of Columns and Column Labels do not match'
    pyplot.legend(args.column_labels)

#set labels
pyplot.xlabel(args.x_label[0])
pyplot.ylabel(args.y_label[0])

#save the figure if we are supposed to, otherwise try to display it
if args.out_file:
    pyplot.savefig(args.out_file)
    print("\nSaved figure to {0}".format(args.out_file))
else:
    pyplot.show()