#! /usr/bin/env python

# Program : create_template.py
# Author  : Peter Uhe, modified from script by Neil Massey
# Updates : 26/10/16 Sarah Sparrow: Updated to include flag for generic restarts or input csv.
# Purpose : create the xml template for the weather@home experiment 
#           This code will create a pair of historical and natural xmls

import os
import xml.dom.minidom as dom
from xml.dom.minidom import getDOMImplementation
from StringIO import StringIO
from ANC import *
import random
import getopt,sys
random.seed(1)	# ensure reproducibility!

from create_xml2_funcs import CreatePertExpts,AddBatchDict,remove_whitespace_nodes
from create_header_funcs import *

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

def make_experiment_xml(prefix,xml_doc,params,restarts,ic_start,ic_end,start_umid,batch):
	# Set start umid  
	anc = ANC()
        anc.Start(start_umid) # next set

        ######## Make expts ##########
	end_umid=CreatePertExpts(xml_doc,params,restarts,ic_start,ic_end,anc)


	# Add the batch info
	batch['first_start_year']=params['model_start_year']
        batch['last_start_year']=params['model_start_year']
        batch['umid_start']=start_umid
        batch['umid_end']=end_umid
        AddBatchDict(xml_doc,batch)

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
	
	count = xml_doc.getElementsByTagName("experiment").length

	print "Number of workunits: ",count

	
##############################
if __name__ == "__main__":
	# Firstly read any command line options
	ProcessCommandLineOpts()

	# Parameters that are the SAME for historical and natural simulations
	base_params={}
	base_params['model_start_year']=2015
	base_params['model_start_month']=12
	base_params['run_years']=0
	base_params['run_months']=7
	base_params['file_solar']='solar_1985_2020'
	base_params['file_volcanic']='volc_1985_2020'
	base_params['file_sulphox']='oxi.addfa'

	# Copy the base parameters into both the historical and natural setup dictionaries
	nat_params=base_params.copy()
	hist_params=base_params.copy()

	# Parameters specific to all historical simulations
	hist_params['file_ozone']='ozone_rcp45_N96_2009_2020v2'
	hist_params['file_sst']='ALLclim_ancil_14months_OSTIA_sst_2015-12-01_2017-01-30'
	hist_params['file_sice']='ALLclim_ancil_14months_OSTIA_ice_2015-12-01_2017-01-30'
	hist_params['file_so2dms']='so2dms_Ev5a_baseCLE_N96_2009_2020'
	hist_params['file_ghg']='ghg_defaults'


	# Parameters specific to all natural simulations
	nat_params['file_ozone']='o3_n96_pers_1959_1999_2020'
	nat_params['file_so2dms']='so2dms_prei_N96_1855_0000P'
	nat_params['file_sst']='NATclim_ancil_14months_OSTIA_sst_MMM_2015-12-01_2016-01-30'
	nat_params['file_sice']='OSICE_natural_0000P'
	nat_params['file_ghg']='file_ghg_1850'

	# Set up the xml doc - Remember to check/alter the header info as required
	expt_types=["actual","natural"]
	impl = getDOMImplementation()
	# Set up doc
        upload_loc="dev"
        app_config="config_wah2.2_eas50.xml"
	region=app_config.split("_")[2].split(".")[0]
	
        # define stash files in the order global,regional (or global only)
        stash_files=["xaakm_global_basic_2016-04-18.stashc","xacxf_region_basic_2016-07-19_v5.stashc"]

	# define the generic restarts
	generic_restarts='xhjlya.start.0000.360.new, generic_start_eas50_aabbw'

	# Otherwise supply a csv list of <global_restart>,<regional_restart> for each experiment and define the number of pairs of restarts.
	existing_restarts={"act":'batch486_restarts.csv',"nat":'batch487_restarts.csv'}

	# Set up number of initial conditions to use within the experiments
        ic_start=0
        ic_end = 3

	filename_prefix='xmls/wu_wah2_'+region+'_'
	if not os.path.exists('xmls'):
	    os.makedirs('xmls')

	print "Creating experiments... "
	for expt_type in expt_types:
		print expt_type.title()+" experiment"
		if expt_type=="actual":
			expt_params=hist_params.copy()
			start_umid = "a000"
		elif expt_type=="natural":
			expt_params=nat_params.copy()
			start_umid = "n000"
		else: 
			raise
        	xml_doc = impl.createDocument(None, "WorkGen", None)
        	root = xml_doc.documentElement

	        make_header(xml_doc,Vars.site,upload_loc,app_config,stash_files)

		# Add in the restart files
		if Vars.generic==True:
			# If the generic flag is set use the generic restarts for all experiments
			restarts_list=generic_restarts
			restart_info="generic"
			desc_info="Spin-up"
			n_restarts=1
		else:
			restarts_list=existing_restarts[expt_type[0:2]]
			restart_info=restarts_list.split("_")[0]
			desc_info="2nd generation"
			n_restarts=52

		# Add in batch tags:
                batch={}
                batch['name']=expt_type.title()+" WAH2 East Asia 50km "+str(expt_params["model_start_year"])
                batch['desc']=desc_info+" "+expt_type+" WAH2 East Asia 50km "+str(expt_params["model_start_year"])
                batch['owner']="Sarah Sparrow <sarah.sparrow@oerc.ox.ac.uk>"
                batch['tech_info']=str(ic_end-ic_start)+" initial condition perturbations per restart, "+str(n_restarts)+" restarts per year from "+restart_info+", forced by OSTIA SSTs and sea-ice"
                batch['proj']='LOTUS'


		######## Make expts ##########
		make_experiment_xml(filename_prefix+expt_type+"_",xml_doc,expt_params,restarts_list,ic_start,ic_end,start_umid,batch)
	
		
	print 'Done!'
	print 'Now please verify the header/batch information before upload'
