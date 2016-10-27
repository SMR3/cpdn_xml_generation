#! /usr/bin/env python

# Program : create_template.py
# Author  : Peter Uhe, modified from script by Neil Massey
# Updates : 26/10/16 Sarah Sparrow: Updated to includ flag for generic restarts or input csv.
# Purpose : create the xml template for the weather@home experiment 
#           This code will create a pair of historical and natural xmls

import xml.dom.minidom as dom
from StringIO import StringIO
from ANC import *
import random
import getopt,sys
random.seed(1)	# ensure reproducibility!

from create_xml2_funcs import CreatePertExpts,AddBatchDict,remove_whitespace_nodes

class Vars:
	#input command line variables
	generic=False
	site=""
	pass


##############################################################################


def Usage():
	print "Usage :	--generic	uses generic restart files\n"\
	"	--site=		specify 'dev' or 'main' site"

	sys.exit()


##############################################################################


def ProcessCommandLineOpts():

        # Process the command line arguments
        try:
                opts, args = getopt.getopt(sys.argv[1:],'',
                ['generic','site='])

                if len(opts) == 0:
                        Usage()
                for opt, val in opts:
                        if opt == '--generic':
                                Vars.generic=True
			elif opt == '--site':
                                Vars.site=val
        except getopt.GetoptError:
                Usage()

##############################################################################

def make_experiment_xml(prefix,xml_doc,params,restarts,ic_start,ic_end,start_umid):
	# Set start umid  
	anc = ANC()
        anc.Start(start_umid) # next set

        ######## Make expts ##########

        end_umid=CreatePertExpts(xml_doc,params,restarts,ic_start,ic_end,anc)

        ######## Write out the file ########
	xml_filename=prefix + str(params['model_start_year']) + "_" +\
                          start_umid + '_' + end_umid + '.xml'
        #define the xml filename
        fh = open(xml_filename, 'w')
        print 'Writing to:',xml_filename,'...'
        remove_whitespace_nodes(xml_doc)
        xml_doc.writexml(fh,newl='\n',addindent='\t')
#xml_doc.writexml(fh)
        fh.close()

	
##############################
if __name__ == "__main__":
	# Firstly read any command line options
	ProcessCommandLineOpts()

	# Parameters that are the SAME for historical and natural simulations
	base_params={}
	base_params['model_start_year']=2013
	base_params['model_start_month']=12
	base_params['run_years']=0
	base_params['run_months']=3
	base_params['file_solar']='solar_1985_2020'
	base_params['file_volcanic']='volc_1985_2020'
	base_params['file_sulphox']='oxi.addfa'

	# Copy the base parameters into both the historical and natural setup dictionaries
	nat_params=base_params.copy()
	hist_params=base_params.copy()

	# Parameters specific to all historical simulations
	hist_params['file_ozone']='ozone_rcp45_N96_2009_2020v2'
	hist_params['file_sst']='final_ancil_2year_OSTIA_sst_2013-12-01_2015-12-30'
	hist_params['file_sice']='final_ancil_2year_OSTIA_ice_2013-12-01_2015-12-30'
	hist_params['file_so2dms']='so2dms_Ev5a_baseCLE_N96_2009_2020'
	hist_params['file_ghg']='ghg_defaults'


	# Parameters specific to all natural simulations
	nat_params['file_ozone']='o3_n96_pers_1959_1999_2020'
	nat_params['file_so2dms']='so2dms_prei_N96_1855_0000P'
	nat_params['file_sst']='delta_ancil_2year_OSTIA_sst_2013-12-01_2015-12-30_MMM'
	nat_params['file_sice']='OSICE_natural_0000P'
	nat_params['file_ghg']='file_ghg_1850'

	# Set up the xml doc - Remember to check/alter the header info as required
	if Vars.site=='dev':
		template='templates/dev_site_header_template.xml'
	elif Vars.site=='main':
		template='templates/main_site_header_template.xml'
	else:
		template='templates/dev_site_header_template.xml'
	xml_doc = dom.parse(template)

	# Set up number of initial conditions to use within the experiments
	ic_start=0
	ic_end = 3

	# Add in the restart files
	if Vars.generic==True:
		# If the generic flag is set use the generic restarts for all experiments
		restarts_list_hist='xhjlya.start.0000.360.new, generic_start_eas50_aabbw'
        	restarts_list_nat='xhjlya.start.0000.360.new, generic_start_eas50_aabbw'
		n_restarts=1
	else:
		# Otherwise supply a csv list of <global_restart>,<regional_restart> for each experiment and define the number of pairs of restarts.
		restarts_list_allforc='batch221_restarts_hist.csv'
		restarts_list_nat='batch221_restarts_nat.csv'
		n_restarts=52

	# Set start umid		
	start_umid_hist = "a000"
	start_umid_nat = "n000"

	print "Creating experiments... "

	filename_prefix_hist='xmls/wu_wah2_hist_'
	filename_prefix_nat='xmls/wu_wah2_nat_'


	######## Make expts ##########
	make_experiment_xml(filename_prefix_hist,xml_doc,hist_params,restarts_list_hist,ic_start,ic_end,start_umid_hist)
	make_experiment_xml(filename_prefix_nat,xml_doc,nat_params,restarts_list_nat,ic_start,ic_end,start_umid_nat)	

	print 'Done!'
	print 'Now please verify the header/batch information before upload'
