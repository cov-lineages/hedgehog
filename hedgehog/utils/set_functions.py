from Bio import SeqIO
from hedgehog.utils.log_colours import green,cyan,red
import collections
import hashlib

def get_lineage_hash_string(lineages):
    blineage = "|".join(lineages).encode()
    lineage_hash = hashlib.md5(blineage)
    set_name = lineage_hash.hexdigest()
    return set_name

def filter_incomplete_spikes(seq):
    complete = True
    for base in str(seq).upper():
        if base not in ["A","T","G","C","-"]:
            complete = False
            break
    return complete

def get_child_dict(lineages):
    child_dict = collections.defaultdict(list)
    alias = {'C': 'B.1.1.1',
            'D': 'B.1.1.25',
            'G': 'B.1.258.2',
            'K': 'B.1.1.277',
            'L': 'B.1.1.10',
            'M': 'B.1.1.294',
            'N': 'B.1.1.33',
            'P': 'B.1.1.28',
            'R': 'B.1.1.316',
            'S': 'B.1.1.217',
            'U': 'B.1.177.60',
            'V': 'B.1.177.54',
            'W': 'B.1.177.53',
            'Y': 'B.1.177.52',
            'Z': 'B.1.177.50',
            'AA': 'B.1.177.15',
            'AB': 'B.1.160.16',
            'AC': 'B.1.1.405',
            'AD': 'B.1.1.315',
            'AE': 'B.1.1.306',
            'AF': 'B.1.1.305',
            'AG': 'B.1.1.297',
            'AH': 'B.1.1.241',
            'AJ': 'B.1.1.240',
            'AK': 'B.1.1.232',
            'AL': 'B.1.1.231',
            'AM': 'B.1.1.216',
            'AN': 'B.1.1.200',
            'AP': 'B.1.1.70',
            'AQ': 'B.1.1.39',
            'AS': 'B.1.1.317',
            "AT": "B.1.1.370",
            "AU": "B.1.466.2",
            "AV": "B.1.1.482"}
            
    for lineage in lineages:
        lineage = lineage.lstrip("*")
        for i in range(len(lineage.split("."))):
            parent = ".".join(lineage.split(".")[:i+1])
            if parent in alias:
                a = alias[parent]
                for i in range(len(a.split("."))):
                    parent2 = ".".join(a.split(".")[:i+1])
                    child_dict[parent2].append(lineage)
            elif "B"==parent:
                child_dict[parent].append(lineage)
                child_dict["A"].append(lineage)
            else:
                child_dict[parent].append(lineage)
    children = {}
    for lineage in child_dict:
        children_lineages = sorted(list(set(child_dict[lineage])))
        children[lineage] = children_lineages
    return children

def get_children(lineage, child_dict):
    return child_dict[lineage]     
            
def get_mrca(lineage1,lineage2,child_dict):
    mrca = "A"
    for lineage in child_dict:
        children = child_dict[lineage]
        if lineage1 in children and lineage2 in children:
            mrca = lineage
    return mrca


