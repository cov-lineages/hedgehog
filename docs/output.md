# Output

hedgehog outputs a csv file with taxon name and lineage set assigned, one line corresponding to each sequence in the fasta file provided. 

## CSV column headers

### taxon

The name of an input query sequence. Note that spaces and commas in sequence names (not a good idea to have these characters in sequence names in general) get replaced by underscores. 

### set_name
6-character long set name that is generated from the lineages that comprise a given set.

### set_hash
The full length extended hash for a given set, used for matching internal to hedgehog.

### precision
The lineage that is the most recent common ancestor of all lineages within a given set.

### set_description
A human readable set description, combining the precision (mrca) and a unique identifier for a given set assignment.

### lineage_count
How many lineages are present in a given lineage set.

### spike_constellation
The spike mutations that define the lineage set.

### conflict
The number of conflicting equally likely assignments.

### ambiguity score
The proportion of potentially informative sites present/missing in a query sequence.

### hedgehog_version
Version of hedgehog software run.

### pango_version
Version of pango designations included in the hedgehog model.

### status
Either passed or failed min_length and max_ambiguity quality control.

### note
Source of assignment, either from designation hash or via the custom pangoLEARN model.


# Example output file
  
```  
taxon,set_name,set_hash,precision,set_description,lineage_count,spike_constellation,conflict,ambiguity_score,hedgehog_version,pango_version,status,note
test_B.1.371,2add08,2add08a569c4004e5d3b21906f8a716f,A,A_1,615,S:D614G,NA,NA,,1.0,v1.2.6,passed_qc,Assigned from designation hash.
test_B.1.617.2,3613c5,3613c54b4a4a42a10036fa7ec340baef,B.1.617.2,B.1.617.2,1,S:D614G|S:L452R|S:P681R|S:T19R|S:T478K,NA,NA,,1.0,v1.2.6,passed_qc,Assigned from designation hash.
test_B.4,bc4a34,bc4a34e19529392c6ad118601e0469c3,A,A_2,75,,0.0,1.0,1.0,v1.2.6,passed_qc,
test_B.1.1.7,2430b9,2430b919e9b5f418c6a13add9d3c1db8,B.1.1.7,B.1.1.7,1,S:A570D|S:D1118H|S:D614G|S:N501Y|S:P681H|S:S982A|S:T716I|del:21765:6|del:21991:3,0.0,1.0,1.0,v1.2.6,passed_qc,
Novel_B.1.617.2,3613c5,3613c54b4a4a42a10036fa7ec340baef,B.1.617.2,B.1.617.2,1,S:D614G|S:L452R|S:P681R|S:T19R|S:T478K,0.0,1.0,1.0,v1.2.6,passed_qc,
test_bad_seq,None,None,NA,NA,NA,NA,NA,NA,1.0,v1.2.6,fail,seq_len:12
```