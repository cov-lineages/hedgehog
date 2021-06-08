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
## Example output file
  
```  
taxon,set_name,set_hash,precision,set_description,lineage_count,spike_constellation,conflict,ambiguity_score,hedgehog_version,pango_version,status,note
test_B.1.371,2add08,2add08a569c4004e5d3b21906f8a716f,A,A_1,615,S:D614G,NA,NA,,1.0,v1.2.6,passed_qc,Assigned from designation hash.
test_B.1.617.2,3613c5,3613c54b4a4a42a10036fa7ec340baef,B.1.617.2,B.1.617.2,1,S:D614G|S:L452R|S:P681R|S:T19R|S:T478K,NA,NA,,1.0,v1.2.6,passed_qc,Assigned from designation hash.
test_B.4,bc4a34,bc4a34e19529392c6ad118601e0469c3,A,A_2,75,,0.0,1.0,1.0,v1.2.6,passed_qc,
test_B.1.1.7,2430b9,2430b919e9b5f418c6a13add9d3c1db8,B.1.1.7,B.1.1.7,1,S:A570D|S:D1118H|S:D614G|S:N501Y|S:P681H|S:S982A|S:T716I|del:21765:6|del:21991:3,0.0,1.0,1.0,v1.2.6,passed_qc,
Novel_B.1.617.2,3613c5,3613c54b4a4a42a10036fa7ec340baef,B.1.617.2,B.1.617.2,1,S:D614G|S:L452R|S:P681R|S:T19R|S:T478K,0.0,1.0,1.0,v1.2.6,passed_qc,
test_bad_seq,None,None,NA,NA,NA,NA,NA,NA,1.0,v1.2.6,fail,seq_len:12
```