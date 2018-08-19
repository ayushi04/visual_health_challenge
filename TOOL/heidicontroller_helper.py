import os
import pandas as pd
import config
from mod_datacleaning import data_cleaning
import heidicontroller_helper as hch

from mod_matrix import generateCustomMatrix as gcm
from mod_matrix import region_label as rg
from mod_matrix import image_module as hd
from mod_matrix import orderPoints as op

from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.plotting import figure, output_file, show
from bokeh.models.widgets import Panel, Tabs
from bokeh.layouts import gridplot


from bokeh_scripts.histogram import histogram_tab
from bokeh_scripts.density import density_tab
from bokeh_scripts.table import table_tab
from bokeh_scripts.draw_map import map_tab
from bokeh_scripts.routes import route_tab


def getMetaInfo(data):
	'''
	cname=list(data.columns)
	for c in cname:
		if c.find('ID')==-1:
			print(c)
	data = {"y": [1, 2, 3, 4, 5]}
	output_file("lines.html", title="line plot example") #put output_notebook() for notebook
	# Here is a list of categorical values (or factors)
	fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']

	# Set the x_range to the list of categories above
	p = figure(x_range=fruits, plot_height=250, title="Fruit Counts")

	# Categorical values can also be used as coordinates
	p.vbar(x=fruits, top=[5, 3, 4, 2, 4, 6], width=0.9)

	# Set some properties to make the plot look better
	p.xgrid.grid_line_color = None
	p.y_range.start = 0
	'''
	# Read data into dataframes
	flights = pd.read_csv('static/flights.csv',index_col=0).dropna()
	# Formatted Flight Delay Data for map
	map_data = pd.read_csv('static/flights_map.csv',header=[0,1], index_col=0)

	tab1 = histogram_tab(flights)
	tab2 = density_tab(flights)
	tab3 = table_tab(flights)
	#tab4 = map_tab(map_data, states)
	#tab5 = route_tab(flights)

	# Put all the tabs into one application
	tabs = Tabs(tabs = [tab1, tab2, tab3])


	return tabs