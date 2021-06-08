#!/usr/bin/env python3
from hedgehog import __version__
from hedgehog import PANGO_VERSION
import argparse
import os.path
import snakemake
import sys
from urllib import request
import subprocess
import json
from tempfile import gettempdir
import tempfile
import pprint
import json
import os
import joblib


from hedgehog.utils import dependency_checks
from hedgehog.utils import data_install_checks

import hedgehog.utils.custom_logger as custom_logger
from hedgehog.utils.log_colours import green,cyan,red

import pkg_resources
from Bio import SeqIO

from . import _program

thisdir = os.path.abspath(os.path.dirname(__file__))
cwd = os.getcwd()

def main(sysargs = sys.argv[1:]):

    parser = argparse.ArgumentParser(prog = _program,
    description='hedgehog: SARS-CoV-2 Spike-sequence based lineage set assignment',
    usage='''hedgehog <query> [options]''')

    parser.add_argument('query', nargs="*", help='Query fasta file of spike sequences to analyse.')
    parser.add_argument('-o','--outdir', action="store",help="Output directory. Default: current working directory")
    parser.add_argument('--outfile', action="store",help="Optional output file name. Default: lineage_set_report.csv")
    parser.add_argument('--tempdir',action="store",help="Specify where you want the temp stuff to go. Default: $TMPDIR")
    parser.add_argument("--no-temp",action="store_true",help="Output all intermediate files, for dev purposes.")
    parser.add_argument('--max-ambig', action="store", default=0.1, type=float,help="Maximum proportion of Ns allowed for hedgehog to attempt assignment. Default: 0.1",dest="maxambig")
    parser.add_argument('--min-length', action="store", default=3790, type=int,help="Minimum query length allowed for hedgehog to attempt assignment. Default: 3800",dest="minlen")
    parser.add_argument('--seq-chunk-size', action="store", default=500, type=int,help="Minimum query length allowed for hedgehog to attempt assignment. Default: 500",dest="seq_chunk_size")
    
    parser.add_argument("--verbose",action="store_true",help="Print lots of stuff to screen")

    parser.add_argument("-t","--threads",action="store",default=1,type=int, help="Number of threads")
    parser.add_argument("-v","--version", action='version', version=f"hedgehog {__version__}")
    parser.add_argument("-pv","--pango-version", action='version', version=f"pango {PANGO_VERSION}")

    if len(sysargs)<1:
        parser.print_help()
        sys.exit(-1)
    else:
        args = parser.parse_args(sysargs)

    dependency_checks.check_dependencies()

    # to enable not having to pass a query if running update
    # by allowing query to accept 0 to many arguments
    if len(args.query) > 1:
        print(cyan(f"Error: Too many query (input) fasta files supplied: {args.query}\nPlease supply one only"))
        parser.print_help()
        sys.exit(-1)
    else:
        # find the query fasta
        query = os.path.join(cwd, args.query[0])
        if not os.path.exists(query):
            sys.stderr.write('Error: cannot find query (input) fasta file at {}\nPlease enter your fasta sequence file and refer to pangolin usage at:\nhttps://github.com/hCoV-2019/pangolin#usage\n for detailed instructions\n'.format(query))
            sys.exit(-1)
        else:
            print(green(f"The query file is:") + f"{query}")

        # default output dir
    outdir = ''
    if args.outdir:
        outdir = os.path.join(cwd, args.outdir)
        if not os.path.exists(outdir):
            try:
                os.mkdir(outdir)
            except:
                sys.stderr.write(cyan(f'Error: cannot create directory:') + f"{outdir}")
                sys.exit(-1)
    else:
        outdir = cwd

    outfile = ""
    if args.outfile:
        outfile = os.path.join(outdir, args.outfile)
    else:
        outfile = os.path.join(outdir, "lineage_set_report.csv")

    tempdir = ''
    if args.tempdir:
        to_be_dir = os.path.join(cwd, args.tempdir)
        if not os.path.exists(to_be_dir):
            os.mkdir(to_be_dir)
        temporary_directory = tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=to_be_dir)
        tempdir = temporary_directory.name
    else:
        temporary_directory = tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=None)
        tempdir = temporary_directory.name

    if args.no_temp:
        print(green(f"\n--no-temp: ") + f"all intermediate files will be written to {outdir}\n")
        tempdir = outdir

    """
    QC steps:
    1) check no empty seqs
    2) check N content
    3) write a file that contains just the seqs to run
    """

    do_not_run = []
    run = []
    total_input = 0
    print(green("** Sequence QC **"))
    fmt = "{:<30}\t{:>25}\t{:<10}\n"

    print("{:<30}\t{:>25}\t{:<10}\n".format("Sequence name","Reason","Value"))
    for record in SeqIO.parse(query, "fasta"):
        total_input +=1
        # replace spaces in sequence headers with underscores
        record.description = record.description.replace(' ', '_')
        record.id = record.description
        if "," in record.id:
            record.id=record.id.replace(",","_")

        if len(record) <args.minlen:
            record.description = record.description + f" fail=seq_len:{len(record)}"
            do_not_run.append(record)
            print(fmt.format(record.id, "Seq too short", len(record)))
            # print(record.id, "\t\tsequence too short")
        else:
            num_N = str(record.seq).upper().count("N")
            prop_N = round((num_N)/len(record.seq), 2)
            if prop_N > args.maxambig:
                record.description = record.description + f" fail=N_content:{prop_N}"
                do_not_run.append(record)
                print(fmt.format(record.id, "N content too high", prop_N))
                # print("{record.id} | has an N content of {prop_N}")
            else:
                run.append(record)

    print(green("\nNumber of sequences detected: ") + f"{total_input}")
    print(green("Total passing QC: ") + f"{len(run)}")

    if run == []:
        with open(outfile, "w") as fw:
            fw.write("taxon,set_name,mrca,set_description,lineage_count,spike_constellation,conflict,ambiguity_score,hedgehog_version,pango_version,status,note\n")
            for record in do_not_run:
                desc = record.description.split(" ")
                reason = ""
                for item in desc:
                    if item.startswith("fail="):
                        reason = item.split("=")[1]
                fw.write(f"{record.id},None,NA,NA,NA,NA,NA,NA,NA,{__version__},{PANGO_VERSION},fail,{reason}\n")
        print(cyan(f'Note: no query sequences have passed the QC\n'))
        sys.exit(0)

    post_qc_query = os.path.join(tempdir, 'query.post_qc.fasta')
    with open(post_qc_query,"w") as fw:
        SeqIO.write(run, fw, "fasta")
    qc_fail = os.path.join(tempdir,'query.failed_qc.fasta')
    with open(qc_fail,"w") as fw:
        SeqIO.write(do_not_run, fw, "fasta")

    config = {
        "query_fasta":post_qc_query,
        "outdir":outdir,
        "outfile":outfile,
        "tempdir":tempdir,
        "qc_fail":qc_fail,
        "seq_chunk_size":args.seq_chunk_size,
        "verbose":args.verbose,
        "hedgehog_version":__version__,
        "pango_version":PANGO_VERSION,
        "threads":args.threads
        }

    data_install_checks.check_install(config)
    snakefile = data_install_checks.get_snakefile(thisdir)
    
    dependency_checks.set_up_verbosity(config)

    if args.verbose:
        print(green("\n**** CONFIG ****"))
        for k in sorted(config):
            print(green(k), config[k])

        status = snakemake.snakemake(snakefile, printshellcmds=True, forceall=True, force_incomplete=True,
                                        workdir=tempdir,config=config, cores=args.threads,lock=False
                                        )
    else:
        logger = custom_logger.Logger()
        status = snakemake.snakemake(snakefile, printshellcmds=False, forceall=True,force_incomplete=True,workdir=tempdir,
                                    config=config, cores=args.threads,lock=False,quiet=True,log_handler=config["log_api"]
                                    )

    if status: # translate "success" into shell exit code of 0
       return 0

    return 1

    sys.exit(0)

if __name__ == '__main__':
    main()
