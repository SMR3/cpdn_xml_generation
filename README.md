# cpdn_xml_generation
Code to generate xml files for workunit submission to the climateprediction.net project


This repository contains basic code for generating an attribution style weather@home experiment and hadcm3s perturbed parameter experiments.

There are two main scripts:
(1) create_basic_attribution.py

This code will create two xmls for actual and natural weather@home simulations
It will need editing to make sure that the correct restart files and forcing files are used
It has the following command line options:
--site=  This should contain either 'dev' or 'main' to specify whether the workunit is for the dev of main sites
--generic This means that generic restart files (specified in the script) are used throughout.


(2) create_basic_hadcm3_xml.py

This code will generate a hadcm3 workunit xml with parameter perturbations taken from an existing data file (in param_data directory)
It has the following command line options:
--site= This should contain either 'dev' or 'main' to specify whether the workunit is for the dev of main sites
--generic This will apply the standard physics restart files throughout
--add_stdp This will ensure that the standard physics configuration is included as a workunit in the xml
--paramids= This should be either a comma separated list of parameter sets OR filename to read parameter sets from default will be all parameter sets in the data structure


Remember to edit the header information so that:
(a) The correct model and region are run
(b) The results are sent to the correct upload server
(c) The batch description is correct




