# cpdn_xml_generation
Code to generate xml files for workunit submission to the climateprediction.net project


This repository contains basic code for generating an attribution style weather@home experiment and hadcm3s perturbed parameter experiments.
This is aimed to give you a starting point for generation scripts that can then be tailored to fit your requirements

There are four main xml generation scripts:

(1) create_basic_attribution.py

This code will create two xmls for actual and natural weather@home simulations
It will need editing to make sure that the correct region,upload server, restart files and forcing files are used
It has the following command line options:

--site=  This should contain either 'dev' or 'main' to specify whether the workunit is for the dev of main sites

--generic This means that generic restart files (specified in the script) are used throughout.

(2) create_basic_spinup_climatology.py

This code will create an xml for a climatology spinup for weather@home simulations
It will need editing to make sure that the correct region, upload server, generic restart files and forcing files are used
It has the following command line options:

--site=  This should contain either 'dev' or 'main' to specify whether the workunit is for the dev of main sites

(3) create_second_generation_climatology.py 

This code will create an xml for a second generation climatology for weather@home simulations
It will need editing to make sure that the correct region, upload sercer, restart file csv and forcing files are used
It has the following command line options:

--site=  This should contain either 'dev' or 'main' to specify whether the workunit is for the dev of main sites

(4) create_basic_hadcm3_xml.py

This code will generate a hadcm3 workunit xml with parameter perturbations taken from an existing data file (in param_data directory)
It has the following command line options:

--site= This should contain either 'dev' or 'main' to specify whether the workunit is for the dev of main sites

--generic This will apply the standard physics restart files throughout

--add_stdp This will ensure that the standard physics configuration is included as a workunit in the xml

--paramids= This should be either a comma separated list of parameter sets OR filename to read parameter sets from default will be all parameter sets in the data structure


IMPORTANT

Remember to edit **all** scripts to specify:

(a) The correct model and region are run

(b) The results are sent to the correct upload server

(c) The batch description is correct and a batch owner is added (for syntax see the project wiki)


Restart file extraction:

Restart files from spinup simulations can be extracted using extract_restarts.py.
This code has the following command line options:

--batch=        batch number to extract restarts from

--data_dir=     location of the batch directories (i.e. the directory containing all the batch directories)

--out_dir=      location to put the extracted restarts in

--model_type=   model type enter 'global', 'coupled' or 'nested'

--dry_run       do a dry run without extracting files

A csv file will be created in the output directory that specifies the names of paired global and regional restart files and can be used with the xml generation scripts to create second generation simulations.




