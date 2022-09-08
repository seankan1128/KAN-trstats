"""
usage: trstats.py [-h] [-n NUM_RUNS] [-d RUN_DELAY] [-m MAX_HOPS] -o OUTPUT -g GRAPH [-t TARGET] [--test TEST_DIR]

Run traceroute multiple times towards a given target host

optional arguments:
  -h, --help       show this help message and exit
  -n NUM_RUNS      Number of times traceroute will run [default: 8]
  -d RUN_DELAY     Number of seconds to wait between two consecutive runs [default: 0]
  -m MAX_HOPS      Number of times traceroute will run [default: 20] 
  -o OUTPUT        Path and name of output JSON file containing the stats
  -g GRAPH         Path and name of output PDF file containing stats graph
  -t TARGET        A target domain name or IP address (required if --test 
                   is absent)             
  --test TEST_DIR  Directory containing num_runs text files, each of which
                   contains the output of a traceroute run. If present, this
                   will override all other options and traceroute will not be
                   invoked. Stats will be computed over the traceroute output
                   stored in the text files
"""

from docopt import docopt
import os
import pandas as pd
import time
import json
import numpy as np
import plotly.express as px

def trt_i_m(TARGET, i, m):
    file_to_delete = open("text" + str(i) + ".txt",'w')
    file_to_delete.close()
    os.system("traceroute " + "-m " +  m  + " " +  TARGET + " >> text" + str(i) + ".txt")


def main():
    # docopt saves arguments and options as key:value pairs in a dictionary
    args = docopt(__doc__, version='DEMO 1.0')
    print(args)
    num = int(args['-n'])
    delay = args['-d']
    hops = args['-m']
    target = args['-t']
    output = args['-o']
    graph = args['-g']
    test = args['--test']

    if args['--test']:

        path = test
        files = [file for file in os.listdir(path) if not file.startswith('.')]
        df_master = pd.read_csv(path+"/"+files[0], sep="  ", skiprows=1, header = None, engine='python')
        df_master.iloc[:,1] = df_master.iloc[:,1].str.split(' ')
        df_master.iloc[:,2] = df_master.iloc[:,2].str.split(' ').str[0]
        df_master.iloc[:,3] = df_master.iloc[:,3].str.split(' ').str[0]
        df_master.iloc[:,4] = df_master.iloc[:,4].str.split(' ').str[0]
        df_master = df_master.transpose()

        files.pop(0)

        for file in files:
            df = pd.read_csv(str(path + "/" + file), sep="  ", skiprows=1, header = None, engine='python')  
            df.iloc[:,2] = df.iloc[:,2].str.split(' ').str[0].astype(float)
            df.iloc[:,3] = df.iloc[:,3].str.split(' ').str[0].astype(float)
            df.iloc[:,4] = df.iloc[:,4].str.split(' ').str[0].astype(float)
            df = df.iloc[:,2:5]
            df = df.transpose()
            df_master = pd.concat((df_master,df))

        df_master = df_master.fillna(value=np.nan)        
        df_master.to_csv("dsa2.csv", index=False)

        data = []
        for col in df_master.columns:
            data.append({  
            "Avg": df_master[col].iloc[2:].astype(float).mean(),
            "Hop": df_master[col][0],
            "Host": df_master[col][1],
            "Max": df_master[col][2:].astype(float).max(),
            "Min": df_master[col][2:].astype(float).min(),
            "Med": df_master[col][2:].astype(float).median()
            })
            
        # Serializing json
        dictionary = {"data":data}
        json_object = json.dumps(dictionary, indent=6)
    
        # Writing to sample.json
        with open(output, "w") as outfile:
            outfile.write(json_object)

        fig = px.box(df_master)
        fig.write_image(graph+'.pdf')


    if args['-t']:
        for i in range(0,num):
            trt_i_m(target,i,hops)
            time.sleep(int(delay)) # Seconds

        df_master = pd.read_csv("text0.txt", sep="  ", skiprows=1, header = None, engine='python')

        df_master.iloc[:,1] = df_master.iloc[:,1].str.split(' ')
        df_master.iloc[:,2] = df_master.iloc[:,2].str.split(' ').str[0]
        df_master.iloc[:,3] = df_master.iloc[:,3].str.split(' ').str[0]
        df_master.iloc[:,4] = df_master.iloc[:,4].str.split(' ').str[0]
        df_master = df_master.transpose()

        for i in range(1,num):
            df = pd.read_csv("text" + str(i) +".txt", sep="  ", skiprows=1, header = None, engine='python')
            df.iloc[:,2] = df.iloc[:,2].str.split(' ').str[0].astype(float)
            df.iloc[:,3] = df.iloc[:,3].str.split(' ').str[0].astype(float)
            df.iloc[:,4] = df.iloc[:,4].str.split(' ').str[0].astype(float)
            df = df.iloc[:,2:5]
            df = df.transpose()
            df_master = pd.concat((df_master,df))

        df_master = df_master.fillna(value=np.nan)
        
        df_master.to_csv("dsa.csv", index=False)

        data = []
        for col in df_master.columns:
            data.append({  
            "Avg": df_master[col].iloc[2:].astype(float).mean(),
            "Hop": df_master[col][0],
            "Host": df_master[col][1],
            "Max": df_master[col][2:].astype(float).max(),
            "Min": df_master[col][2:].astype(float).min(),
            "Med": df_master[col][2:].astype(float).median()
            })
            
        # Serializing json
        dictionary = {"data":data}
        json_object = json.dumps(dictionary, indent=6)
    
        # Writing to sample.json
        with open(output, "w") as outfile:
            outfile.write(json_object)

        fig = px.box(df_master)
        fig.write_image(graph+'.pdf')
        
if __name__=='__main__':
    main()