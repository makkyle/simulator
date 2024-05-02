import argparse
import os
import subprocess
import sys
import time
from binding_score_measure import *

sys.path.append("C:/Users/harol/Downloads/peter's proposal/YCFS_proposal_material/BCR_cluster/simulator_proof/mutation_pipeline/XBCR_net_main")
print(sys.path)
# time.sleep(10)


# , check_data, extract_data
# import pred_bcr
parser = argparse.ArgumentParser()


#============================================================================================================

parser.add_argument(
    "--execute",
    "-e",
    default = True,
    required= False
)


args = parser.parse_args()


os.getcwd()
print(os.getcwd())

cwd_path = os.getcwd()

## binding_score ##
data= extract_data(cwd_path)
# time.sleep(10)
print(data.head(15))
print(type(data))

    # print(os.getcwd())

heavy = ''
light = ''
antigen = ''


for i in range(len(data)):
    check_bool = check_data(data, i)
    if check_bool == True:
        print('True')
        ## extract the info on heavy chain, light chain and antigen seq from Nature.LTE file
        H,L,A = extract_columns(data,i)
        print(os.getcwd())
        print('heavy',H)
        print('light',L)
        print('antigen',A)
        
        heavy,light,antigen = pass_seq_values(H,L,A)
        # from XBCR_net_main.pred_bcr import *
        print('change_path_step1')
        change_path_step1(cwd_path)
        print(os.getcwd())
        
        ## define the arguments in argparse for operating the pred_bcr.py script
        arg1 = str(H)
        arg2 = str(L)
        arg3 = str(A)
        arg4 = 'XBCR_net'
        arg5 = 'binding'
        arg6 = '0'
        ## run the pred_bcr.py script using subprocess command
        result = subprocess.run(['python','pred_bcr.py','--heavy',arg1,'--light',arg2,'--antig',arg3,
                          '--model_name',arg4,'--data_name',arg5,'--model_num',arg6],capture_output=True,
                          text=True).stdout.strip("\n")
        print('result from subprocess.run')
        ## extract the binding_score (as supposedly it is the last 15 characters in this string)
        print(result[-15:])
        string = result[-15:]
        binding_score = extract_binding_score(string)[0]
        binding_score = str(binding_score)
        ## convert the exponentials to float numbers
        if "e" in binding_score:
            binding_score = process_exponent(binding_score)
            binding_score = float(binding_score)
        else:
            binding_score = float(binding_score)
        print(binding_score)
        index= i
        print('current_index',index)
        ## insert the binding score to its respective cell in the Nature.LTE.xlsx excel file
        df_changed,df = pass_binding_score(data,index,binding_score)
        print(df_changed)
        print(df.head(20))
        print(sys.path)
        # time.sleep(5)
        print(os.getcwd())
        
        print('-------- step 1 ends -----------------------------')
        
        # time.sleep(2)
    elif check_bool == False:
        print('False')
        # time.sleep(100)
        # continue

    if check_step2(data,i) == True:
        print('---------step 2 -- evolution ---------------------')
        current_path = os.getcwd()
        print(current_path)
        # time.sleep(10)
        ## define the protein sequence for inputting into the efficient-evolution process
        H,L,A = extract_columns(data,i)
        arg1 = str(H)
        arg2 = str(L)
        sequence = arg1 + arg2
        print('sequence to input :',sequence)
        ## change current working directory to '/efficient-evolution'
        # current_path = os.getcwd()
        change_path_step2(current_path)

        ## execute the command for evolution estimation for each sequence (heavy chain + light chain)
        result_s2 = subprocess.run(['python','bin/recommend.py',' ',sequence])
        print('result from subprocess.run')
        print(result_s2)



    else:
        print('nothing for step 2')
    








