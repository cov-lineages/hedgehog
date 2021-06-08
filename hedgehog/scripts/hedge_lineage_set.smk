import csv
from Bio import SeqIO
import os
from hedgehog.utils import assignment_hash

import pangolin
import pangolin.pangolearn.pangolearn as pangolearn


rule all:
    input:
        config["outfile"],
        os.path.join(config["tempdir"],"hash_assigned.csv")


rule align_to_reference:
    input:
        fasta = config["query_fasta"],
        reference = config["spike_reference"],
        snakefile = os.path.join(workflow.current_basedir,"parallel_align.smk")
    output:
        fasta = os.path.join(config["tempdir"],"sequences.aln.fasta"),
        target = os.path.join(config["tempdir"],"alignments","target.txt")
    run:
        seq_count = 0
        sub_seqs = 0
        records = []
        for record in SeqIO.parse(input.fasta,"fasta"):
            seq_count+=1
            records.append(record)
            if seq_count%500 ==0:
                with open(os.path.join(config["tempdir"],"alignments", f"subseqs_{sub_seqs}.fasta"), "w") as fw:
                    SeqIO.write(records, fw, "fasta")
                sub_seqs +=1
                records = []
        if records:
            with open(os.path.join(config["tempdir"],"alignments", f"subseqs_{sub_seqs}.fasta"), "w") as fw:
                SeqIO.write(records, fw, "fasta")

        if seq_count >= config["seq_chunk_size"]:
            shell("snakemake --nolock --snakefile {input.snakefile:q} "
                            "--forceall  "
                            "{config[log_string]}"
                            "--directory {config[tempdir]:q} "
                            "--config "
                            "tempdir={config[tempdir]:q} "
                            f"nums={sub_seqs} "
                            "spike_reference={config[spike_reference]} "
                            "--cores {workflow.cores}")
        else:
            shell("""
            mafft --quiet --add  {input.fasta:q} \
            --keeplength \
            {input.reference:q} \
            > {output.fasta:q} && touch {output.target:q}
            """)

rule hash_sequence_assign:
    input:
        fasta = rules.align_to_reference.output.fasta
    output:
        designated = os.path.join(config["tempdir"],"hash_assigned.csv"),
        for_pangolearn = os.path.join(config["tempdir"],"not_assigned.fasta")
    run:
        set_hash = {}
        with open(config["designated_hash"],"r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                set_hash[row["seq_hash"]] = row["set_hash"]
        
        with open(output.designated,"w") as fw:
            fw.write("taxon,set_hash\n")
            with open(output.for_pangolearn, "w") as fseq:
                for record in SeqIO.parse(input.fasta, "fasta"):
                    if record.id!="reference":
                        hash_string = assignment_hash.get_hash_string(record)
                        if hash_string in set_hash:
                            fw.write(f"{record.id},{set_hash[hash_string]}\n")
                        else:
                            fseq.write(f">{record.description}\n{record.seq}\n")

rule pangolearn:
    input:
        fasta = rules.hash_sequence_assign.output.for_pangolearn,
        model = config["trained_model"],
        header = config["header_file"],
        reference = config["spike_reference"]
    output:
        os.path.join(config["tempdir"],"lineage_report.pass_qc.csv")
    run:
        pangolearn.assign_lineage(input.header,input.model,input.reference,input.fasta,output[0])

rule add_failed_seqs:
    input:
        qcpass= os.path.join(config["tempdir"],"lineage_report.pass_qc.csv"),
        designated = rules.hash_sequence_assign.output.designated,
        qcfail= config["qc_fail"],
        qc_pass_fasta = config["query_fasta"]
    output:
        csv= config["outfile"]
    run:
        # precision,set_description,lineage_count,spike_constellation,lineages

        set_info = {}
        with open(config['set_info'],"r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                set_info[row["set_hash"]] = row

        fw = open(output.csv,"w")
        fw.write("taxon,set_name,set_hash,precision,set_description,lineage_count,spike_constellation,conflict,ambiguity_score,hedgehog_version,pango_version,status,note\n")
        passed = []

        with open(input.designated,"r") as f:
            reader = csv.DictReader(f)
            note = "Assigned from designation hash."
            for row in reader:

                this_set_info = set_info[row["set_hash"]]
                fw.write(f"{row['taxon']},{row['set_hash'][:6]},{row['set_hash']},{this_set_info['precision']},{this_set_info['set_description']},{this_set_info['lineage_count']},{this_set_info['spike_constellation']},NA,NA,,{config['hedgehog_version']},{config['pango_version']},passed_qc,{note}\n")
                
        with open(input.qcpass, "r") as f:
            reader = csv.DictReader(f)

            for row in reader:
                note = ''

                support =  1 - round(float(row["score"]), 2)
                
                non_zero_ids = row["non_zero_ids"].split(";")
                if len(non_zero_ids) > 1:
                    note = f"Alt assignments: {row['non_zero_ids']},{row['non_zero_scores']}"
                
                this_set_info = set_info[row["prediction"]]
                fw.write(f"{row['taxon']},{row['prediction'][:6]},{row['prediction']},{this_set_info['precision']},{this_set_info['set_description']},{this_set_info['lineage_count']},{this_set_info['spike_constellation']},{support},{row['imputation_score']},{config['hedgehog_version']},{config['pango_version']},passed_qc,{note}\n")
                passed.append(row['taxon'])

        for record in SeqIO.parse(input.qcfail,"fasta"):
            desc_list = record.description.split(" ")
            note = ""
            for i in desc_list:
                if i.startswith("fail="):
                    note = i.lstrip("fail=")

            fw.write(f"{record.id},None,None,NA,NA,NA,NA,NA,NA,{config['hedgehog_version']},{config['pango_version']},fail,{note}\n")
        
        fw.close()