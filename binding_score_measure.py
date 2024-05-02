import pandas as pd
import numpy as np
import os
import sys
import re
import decimal

## import the heavy, light and antigen data 
def extract_data(data_path):
    data = pd.read_excel(os.path.join(data_path,'Nature_LTE.xlsx'),engine='openpyxl')
    data_df = pd.DataFrame(data)

    return data_df

## check if there is binding score for that row of data
def check_data(data,index):
    if  pd.isna(data['binding_score'][index]):
        # type(data['binding_score'][index]) != float and
        return True
    else:
        return False
        
def extract_columns(data,index):
    heavy = data['Heavy'][index]
    light = data['Light'][index]
    antigen = data['variant_seq'][index]
    antigen = antigen.split('\n')
    antigen = antigen[0]
    return [heavy,light,antigen]

def change_path_step1(data_path):
    os.chdir(os.path.join(data_path,'XBCR_net_main'))
    # os.chdir('XBCR-net-main')

heavy = ''
light = ''
antigen = ''

def pass_seq_values(arg1,arg2,arg3):
    global heavy
    global light
    global antigen
    
    heavy = arg1
    light = arg2 
    antigen = arg3

    return heavy,light,antigen

def extract_binding_score(string):
    selected_string = string[-15:]
    potential_float = re.findall("\d+\.\d+",selected_string)
    return potential_float


def process_exponent(value):
    x = str(value)
    ## extract the last two digits of the value (e.g. 10) after the exponent sign (e)
    x = x[-2:]
    x = int(x)
    # print(x)
    # print(f'%.{x}f' % value)
    ## convert the exponent to float number based on the x after e
    return f'%.{x}f' % value

def pass_binding_score(data,index,binding_score):
    data['binding_score'][index] = binding_score
    data.to_excel("C:/Users/harol/Downloads/peter's proposal/YCFS_proposal_material/BCR_cluster/simulator_proof/mutation_pipeline/Nature_LTE.xlsx",engine='openpyxl')
    return data.loc[index,'binding_score'],data

def check_step2(data,index):
    if  pd.isna(data['evolution'][index]):
        # type(data['binding_score'][index]) != float and
        return True
    else:
        return False

def change_path_step2(data_path):
    os.chdir(os.path.join(data_path,'efficient-evolution'))

    
