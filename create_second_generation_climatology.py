#! /usr/bin/env python

# Program : create_template.py
# Author  : Peter Uhe, modified from script by Neil Massey
# Purpose : create the xml template for the HadAM3P experiment

import xml.dom.minidom as dom
from StringIO import StringIO
from ANC import *
import random
import getopt,sys
random.seed(1)  # ensure reproducibility!

from create_xml2_funcs import CreatePertExpts,AddBatchDict,remove_whitespace_nodes

class Vars:
        #input command line variables
        generic=False
        site=""
        pass


##############################################################################


def Usage():
        print "Usage :  --generic       uses generic restart files\n"\
        "       --site=         specify 'dev' or 'main' site"

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


##############################
if __name__ == "__main__":
	# Firstly process command line options
	ProcessCommandLineOpts()

	# Forcing Parameters for simulations
	params={}
	params['model_start_month']=12
	params['run_years']=1
	params['run_months']=1
	params['file_solar']='solar_1985_2020'
	params['file_volcanic']='volc_1985_2020'
	params['file_sulphox']='oxi.addfa'
	params['file_ghg']='ghg_defaults'
	params['restart_upload_month']=12

	# Set up doc
	template='templates/wu_template_eas50_main.xml'
	xml_doc = dom.parse(template)

	# Set up number of perturbations 
	pert_start=0
	pert_end = 6
	
	first_year=1986
	last_year=2015


	# Set start umid		
	start_umid = "a000"
	anc = ANC()
	anc.Start(start_umid) # next set

	restarts_list='batch_lists/batch_486_restarts.csv'

	print "Creating experiments... "

	# Possible ozone/so2dms files (depending on decade)
	ozone_files={1980:'ozone_hist_N96_1979_1990v2',1990:'ozone_hist_N96_1989_2000v2',2000:'ozone_rcp45_N96_1999_2010v2',2010:'ozone_rcp45_N96_2009_2020v2'}
	so2dms_files={1980:'so2dms_hist_N96_1979_1990v2',1990:'so2dms_hist_N96_1989_2000v2',2000:'so2dms_rcp45_N96_1999_2010',2010:'so2dms_rcp45_N96_2009_2020'}

	for year in range(first_year,last_year+1):
        	i=0
                for restarts in open(restarts_list):
                        if i>=40: # Take only 40 restarts per year
                                break
                        if restarts.split(',')[0].find('_'+str(year)+'-')==-1:
                                continue # The restart isn't for this year. 

                        params['model_start_year']=year
                        decade=(year+1)/10*10
                        params['file_ozone']=ozone_files[decade]
                        params['file_so2dms']=so2dms_files[decade]
        		params['file_sst']='ALLclim_ancil_14months_OSTIA_sst_'+str(year)+'-12-01_'+str(year+2)+'-01-30'
                        params['file_sice']='ALLclim_ancil_14months_OSTIA_ice_'+str(year)+'-12-01_'+str(year+2)+'-01-30'

                        end_umid=CreatePertExpts(xml_doc,params,restarts,pert_start,pert_end,anc)
                        i=i+1

	
	# Add in batch tags:
	batch={}
	batch['name']="WAH2 East Asia 50km 1987-2015"
	batch['desc']="2nd generation WAH2 East Asia 50km climatology for 1987-2015 (starting dec 1986)"
	batch['owner']="Sarah Sparrow <sarah.sparrow@oerc.ox.ac.uk>"
	batch['tech_info']="6 initial condition perturbations per restart per year, 40 restarts per year from batch 486, forced by OSTIA SSTs and sea-ice"
	batch['proj']='LOTUS'
	batch['first_start_year']=first_year
	batch['last_start_year']=last_year
	batch['umid_start']=start_umid
	batch['umid_end']=end_umid
	AddBatchDict(xml_doc,batch)
	
	######## Write out the file ########

        xml_out='wu_wah2_eas50_gen2_climatology_main'+str(first_year)+'-' + str(params['model_start_year']) + "_" +\
                          start_umid + '_' + end_umid + '.xml'
        fh = open("xmls/"+xml_out, 'w')
        print 'Writing to:',xml_out,'...'
        #remove_whitespace_nodes(xml_doc)
        xml_doc.writexml(fh)#,newl='\n',addindent='\t')
        fh.close()
        print 'Done!'
