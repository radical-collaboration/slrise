# GMSLR projection program used for IPCC WG1 AR5
# Translated from IDL to Python 2.7 by Jonathan Gregory 23.10.19
# Adapted for use in FACTS by Gregory Garner 20 November 2019

import os
import argparse
import pickle
import numpy as np

def ar5_fit_glaciersfair(pipeline_id):
	
	# Read in the preprocessed data
	data_file = "{}_data.pkl".format(pipeline_id)
	try:
		f = open(data_file, 'rb')
	except:
		print("Cannot open data file\n")
	
	# Extract the data variables
	my_config = pickle.load(f)
	f.close()
	
	startyr = my_config["startyr"]
	
	# mm yr-1 in Marzeion's CMIP5 ensemble mean for AR5 ref period
	dmzdtref=0.95 
	
	# m from glacier at start wrt AR5 ref period
	dmz=dmzdtref*(startyr-2005)*1e-3 
	
	# random methodological error
	cvgl=0.15
	
	# initial glacier mass, used to set a limit, from Tab 4.2
	glmass=412.0-96.3 
	glmass=1e-3*glmass # m SLE

	# Calibrated parameters for glacier methods
	glparm=[dict(name='SLA2012',factor=3.39,exponent=0.722,cvgl=0.15),\
		dict(name='MAR2012',factor=4.35,exponent=0.658,cvgl=0.13),\
		dict(name='GIE2013',factor=3.57,exponent=0.665,cvgl=0.13),\
		dict(name='RAD2014',factor=6.21,exponent=0.648,cvgl=0.17),\
		dict(name='GloGEM',factor=2.88,exponent=0.753,cvgl=0.13)]
	
	# Write the fitted parameters to a pickle file
	output = {'dmz': dmz, 'cvgl': cvgl, 'glmass': glmass, 'glparm': glparm}
	
	# Write the configuration to a file
	outdir = os.path.dirname(__file__)
	outfile = open(os.path.join(outdir, "{}_fit.pkl".format(pipeline_id)), 'wb')
	pickle.dump(output, outfile)
	outfile.close()
	
	return(0)



if __name__ == '__main__':
	
	# Initialize the command-line argument parser
	parser = argparse.ArgumentParser(description="Run the glaciers fitting stage for the AR5 SLR projection workflow",\
	epilog="Note: This is meant to be run as part of the Framework for the Assessment of Changes To Sea-level (FACTS)")
	
	# Define the command line arguments to be expected
	parser.add_argument('--pipeline_id', help="Unique identifier for this instance of the module")
	
	# Parse the arguments
	args = parser.parse_args()
	
	# Run the fitting process with the provided command line arguments
	ar5_fit_glaciersfair(args.pipeline_id)
	
	exit()