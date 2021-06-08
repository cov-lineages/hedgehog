#!/usr/bin/env python3
import pkg_resources
from hedgehog.utils import log_colours as colour
import sys
import os


def package_data_check(filename,directory,key,config):
    try:
        package_datafile = os.path.join(directory,filename)
        data = pkg_resources.resource_filename('hedgehog', package_datafile)
        config[key] = data
    except:
        sys.stderr.write(colour.cyan(f'Error: Missing package data.')+f'\n\t- {filename}\nPlease install the latest hedgehog version with `hedgehog --update`.\n')
        sys.exit(-1)

def get_snakefile(thisdir):
    snakefile = os.path.join(thisdir, 'scripts','hedge_lineage_set.smk')
    if not os.path.exists(snakefile):
        sys.stderr.write(cyan(f'Error: cannot find Snakefile at {snakefile}\n Check installation\n'))
        sys.exit(-1)
    return snakefile

def check_install(config):
    resources = [
        {"key":"reference_fasta",
        "directory":"data",
        "filename":"reference.fasta"},
        {"key":"spike_reference",
        "directory":"data",
        "filename":"reference_spike.fasta"},
        {"key":"genbank_ref",
        "directory":"data",
        "filename":"reference.gb"},
        {"key":"header_file",
        "directory":"data",
        "filename":"decisionTreeHeaders_v1.joblib"},
        {"key":"trained_model",
        "directory":"data",
        "filename":"decisionTree_v1.joblib"},
        {"key":"designated_hash",
        "directory":"data",
        "filename":"sets.hash.csv"},
        {"key":"set_info",
        "directory":"data",
        "filename":"set_names.95.csv"}
        
    ]
    for resource in resources:
        package_data_check(resource["filename"],resource["directory"],resource["key"],config)

# config={}
# check_install()
