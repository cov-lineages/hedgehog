# hedgehog
Spikey SARS-CoV-2 sequence based lineage set assignment

```
usage: hedgehog <query> [options]
  
hedgehog: SARS-CoV-2 Spike-sequence based lineage set assignment

positional arguments:
  query                 Query fasta file of spike sequences to analyse.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTDIR, --outdir OUTDIR
                        Output directory. Default: current working directory
  --outfile OUTFILE     Optional output file name. Default: lineage_set_report.csv
  --tempdir TEMPDIR     Specify where you want the temp stuff to go. Default: $TMPDIR
  --no-temp             Output all intermediate files, for dev purposes.
  --max-ambig MAXAMBIG  Maximum proportion of Ns allowed for hedgehog to attempt assignment. Default: 0.1
  --min-length MINLEN   Minimum query length allowed for hedgehog to attempt assignment. Default: 3800
  --verbose             Print lots of stuff to screen
  -t THREADS, --threads THREADS
                        Number of threads
  -v, --version         show program's version number and exit
  ```
  
 
