#! /usr/bin/env python

# Program : create_template.py
# Author  : Peter Uhe, modified from script by Neil Massey
# Purpose : create the xml template for the HadAM3P experiment

import os
import xml.dom.minidom as dom
from xml.dom.minidom import getDOMImplementation
from StringIO import StringIO
from ANC import *
import random
import getopt,sys
random.seed(1)  # ensure reproducibility!

from create_xml2_funcs import CreatePertExpts,AddBatchDict,remove_whitespace_nodes
from create_header_funcs import *

class Vars:
        #input command line variables
        site=""
        pass


##############################################################################


def Usage():
        print "Usage :   --site=         specify 'dev' or 'main' site"
        sys.exit()


##############################################################################


def ProcessCommandLineOpts():

        # Process the command line arguments
        try:
                opts, args = getopt.getopt(sys.argv[1:],'',
                ['site='])

                if len(opts) == 0:
                        Usage()
                for opt, val in opts:
                        if opt == '--site':
                                Vars.site=val
        except getopt.GetoptError:
                Usage()


##############################
if __name__ == "__main__":
	# Firstly process command line options
	ProcessCommandLineOpts()

	# Forcing Parameters for simulations
	params={}
	params['model_start_month']=8
	params['run_years']=1
	params['run_months']=1
	params['file_solar']='solar_marius_2065_2105v2'
	params['file_volcanic']='volc_marius_2065_2105v2'
	params['file_sulphox']='oxi.addfa'
	params['file_ghg']='CRED_ghg_RCP26_v3_2105'
	params['restart_upload_month']=12

	# Set up doc
        upload_loc="upload4"
	region="anz50"
        app_config="config_wah2.2_"+region+".xml"
        
	# define stash files in the order global,regional (or global only)
        stash_files=["xaakm.anz.stashc.clim.global_v2","xaakg.anz.stashc.clim.region_v2"]

        impl = getDOMImplementation()

        xml_doc = impl.createDocument(None, "WorkGen", None)
        root = xml_doc.documentElement

        make_header(xml_doc,Vars.site,upload_loc,app_config,stash_files)

	# Set up number of perturbations 
	pert_start=0
	if Vars.site=="main":
		pert_end = 6
		nrestarts=40 # Take only 40 restarts per year
	if Vars.site=="dev":
		pert_end = 1 # Use 1 initial condition perturbation
		nrestarts=1 # Take only 1 restart per year
	

	first_year=2090
	last_year=2099


	# Set start umid		
	start_umid = "j000"
	anc = ANC()
	anc.Start(start_umid) # next set

        # Define the restart csv file to use
	restarts_list='batch_lists/batch_639_restarts.csv'

	print "Creating experiments... "

	# Possible ozone/so2dms files (depending on decade)
	ozone_files={1980:'ozone_hist_N96_1979_1990v2',1990:'ozone_hist_N96_1989_2000v2',2000:'ozone_rcp45_N96_1999_2010v2',2010:'ozone_rcp45_N96_2009_2020v2'}
	so2dms_files={1980:'so2dms_hist_N96_1979_1990v2',1990:'so2dms_hist_N96_1989_2000v2',2000:'so2dms_rcp45_N96_1999_2010',2010:'so2dms_rcp45_N96_2009_2020'}

	for year in range(first_year,last_year+1):
        	i=0
                for restarts in open(restarts_list):
                        if i>=nrestarts: # Take only nrestarts per year
                                break
                        if restarts.split(',')[0].find('_'+str(year)+'-')==-1:
                                continue # The restart isn't for this year. 

                        params['model_start_year']=year
                        decade=(year+1)/10*10
#                        params['file_ozone']=ozone_files[decade]
                        params['file_ozone']='ozone_rcp26_N96_2089_2100v2'
#                        params['file_so2dms']=so2dms_files[decade]
                        params['file_so2dms']='so2dms_rcp26_N96_2089_2100'
#        		params['file_sst']='ALLclim_ancil_14months_OSTIA_sst_'+str(year)+'-12-01_'+str(year+2)+'-01-30'
                        params['file_sst']='HAPPI15C_ancil_146months_OSTIA_sst_MMM_2088-12-01_2101-01-30'
#                        params['file_sice']='ALLclim_ancil_14months_OSTIA_ice_'+str(year)+'-12-01_'+str(year+2)+'-01-30'
		        params['file_sice']='HAPPI15C_ancil_146months_NEIL_ice_MMM_2088-12-01_2101-01-30'

                        end_umid=CreatePertExpts(xml_doc,params,restarts,pert_start,pert_end,anc)
                        i=i+1

	
	# Add in batch tags:
	batch={}
	batch['name']="WAH2 ANZ50 HAPPI1.5 2nd gen 2090-2100"
	batch['desc']="2nd gen WAH2 ANZ50 HAPPI1.5 2090-2100 (starting Aug 2090)"
	batch['owner']="Suzanne Rosier <suzanne.rosier@niwa.co.nz>,Sarah Sparrow <sarah.sparrow@oerc.ox.ac.uk>"
	batch['tech_info']="6 initial condition perturbations per restart per year, 40 restarts per year from batch 639, forced by OSTIA SSTs and sea-ice"
	batch['proj']='MELBOURNE'
	batch['first_start_year']=first_year
	batch['last_start_year']=last_year
	batch['umid_start']=start_umid
	batch['umid_end']=end_umid
	AddBatchDict(xml_doc,batch)
	
	######## Write out the file ########

        xml_out='wu_wah2_'+region+'_HAPPI15_gen2_'+Vars.site+str(first_year)+'-' + str(params['model_start_year']) + "_" +\
                          start_umid + '_' + end_umid + '.xml'
        if not os.path.exists('xmls'):
	            os.makedirs('xmls')
	fh = open("xmls/"+xml_out, 'w')
        print 'Writing to:',xml_out,'...'
        remove_whitespace_nodes(xml_doc)
        xml_doc.writexml(fh,newl='\n',addindent='\t')
        fh.close()
       
	# Print out the number of xmls
        count = xml_doc.getElementsByTagName("experiment").length 
        print "Number of workunits: ",count
	
	print 'Done!'
