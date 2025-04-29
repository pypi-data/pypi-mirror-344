"""
Created on Wed Feb 19 12:28:05 2025

@author: gabore
"""

import sys
import gzip
import csv
import math
import statistics
from collections import defaultdict

def get_var_name(var):
    for name, value in globals().items():
        if value is var:
            return name

def DivirstiyCalc(List_p, type):
    calclist = []
    if type == "Shan" or type == 1:
        for p in List_p:
                if p != 0:
                    calclist.append(p*math.log(p))
        return  -sum(calclist)

    elif type == "ExpHet" or type == 2:
        for p in List_p:
                if p != 0:
                    calclist.append(p**2)
        return  1-sum(calclist)           

def readVCF(VCF_file1, VCF_file2):

    fileMerged = defaultdict(list)

    

    with gzip.open(VCF_file1, mode='rt') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t')
        for row in csvreader:
            if str(row[0]) == "#CHROM":
                file1 =  defaultdict(str)
                Sample1_name = row[9]
            if row[0][0] !=  "#":
                if "." not in row[9][0:3]:
                    file1[str(row[0])+str(row[1])] = row[9][0:3]
    with gzip.open(VCF_file2, mode='rt') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t')
        for row in csvreader:
            if str(row[0]) == "#CHROM":
                file2 =  defaultdict(str)
                Sample2_name = row[9]
            if row[0][0] !=  "#":
                if "." not in row[9][0:3]:
                    file2[str(row[0])+str(row[1])] = row[9][0:3]



    for d in (file1, file2):
        for key, value in d.items():
            fileMerged[key].append(value)
    for k, v in list(fileMerged.items()):
        if len(v) < 2:
            del fileMerged[k]

    return fileMerged, Sample1_name, Sample2_name



def Similarity(VCF_file1, VCF_file2, method):
    inputdata, sample1, sample2 = readVCF(VCF_file1, VCF_file2)

    N_Loc = 0
    
    GTp00 = 0
    GTp01 = 0
    GTp11 = 0

    PerLocD = []
    for k, v in list(inputdata.items()):
            if len(v) > 1:
                N_Loc += 1
                if v[0] == "0/0":
                    GTp00 += 1
                if v[0] == "0/1":
                    GTp01 += 1
                if v[0] == "1/1":
                    GTp11 += 1
                if v[1] == "0/0":
                    GTp00 += 1
                if v[1] == "0/1":
                    GTp01 += 1
                if v[1] == "1/1":
                    GTp11 += 1

                        
                GTl00 = 0
                GTl01 = 0                           
                GTl11 = 0


                if v[0] == "0/0":
                    GTl00 += 1
                if v[0] == "0/1":
                    GTl01 += 1
                if v[0] == "1/1":
                    GTl11 += 1
                if v[1] == "0/0":
                    GTl00 += 1
                if v[1] == "0/1":
                    GTl01 += 1
                if v[1] == "1/1":
                    GTl11 += 1

                                    

                GTlTOTAL = GTl00 + GTl01 + GTl11
                
                    
                if GTlTOTAL > 1:
                    Dl = DivirstiyCalc([GTl00/GTlTOTAL,GTl01/GTlTOTAL,GTl11/GTlTOTAL], method)
                    PerLocD.append(Dl)
                    

            
    GTpTOTAL = GTp00 + GTp01 + GTp11

    Dp = DivirstiyCalc([GTp00/GTpTOTAL, GTp01/GTpTOTAL, GTp11/GTpTOTAL], method)  
    
    Sim = (Dp-statistics.mean(PerLocD))/Dp

    if N_Loc < 200000:
        print("WARNING: Low number of loci used - the more the merrier")


    print("Sample1","Sample2","Similarity", "Pooled diversity", "N_Loc")
    print(sample1, sample2, Sim, Dp, N_Loc)


    return [sample1, sample2, Sim, Dp, N_Loc] #["Sample1","Sample2","Similarity", "Pooled diversity", "N_Loc"]
 