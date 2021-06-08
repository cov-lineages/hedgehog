list_of_nums = list(range(0,config["nums"]+1))

from Bio import SeqIO

rule all:
    input:
        os.path.join(config["tempdir"],"sequences.aln.fasta")

rule align_to_reference:
    input:
        fasta = os.path.join(config["tempdir"],"alignments/subseqs_{num}.fasta"),
        reference = config["spike_reference"]
    output:
        fasta = os.path.join(config["tempdir"],"alignments/subseqs_{num}.aln.fasta")
    shell:
        """
        mafft --quiet --add  {input.fasta:q} \
        --keeplength \
        {input.reference:q} \
        > {output.fasta:q}
        """
    
rule gather:
    input:
        expand(os.path.join(config["tempdir"],"alignments/subseqs_{num}.aln.fasta"), num=list_of_nums)
    output:
        fasta = os.path.join(config["tempdir"],"sequences.aln.fasta"),
        target = os.path.join(config["tempdir"],"alignments","target.txt")
    run:
        with open(output.fasta,"w") as fw:
            for sub_aln in input:
                for record in SeqIO.parse(sub_aln, "fasta"):
                    if record.id != "reference":
                        fw.write(f">{record.id}\n{record.seq}\n")
        shell("touch {output.target:q}")
