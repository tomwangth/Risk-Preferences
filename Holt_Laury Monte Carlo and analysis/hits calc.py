import csv
import ast
import pandas as pd
import re
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

#pull data out from csv file
class Receive_Data(object):
    def __init__(self):
        self.theta_list = []
        self.delta_list = []
        self.num_A = 0
        self.result_list = []

    def open_file(self, file_name):

        with open(file_name) as f:
            reader = csv.reader(f)
            for row in reader:
                temp_list = row
                for item in ast.literal_eval(row[4]):
                    if "A" in item:
                        self.num_A += 1
                temp_list.append(self.num_A)
                self.num_A = 0
                self.result_list.append(temp_list)
        return self.result_list

"""this result list adds num_A to the dict, ready for making dataframe"""
#need to add a column of hits in dataframe


result_list = Receive_Data().open_file("Holt_Laury_Output raw1.csv")

#print("result_list:", result_list)

#pair = run
#every run has 10 observations

# reorganize the data in df
class DataFrame(object):
    def __init__(self):
        self.result_list = Receive_Data().open_file("Holt_Laury_Output raw1.csv")
        self.total_row = len(self.result_list)
        self.index_range = range(1,self.total_row+1) # rearrange index of df
        self.df = None
        self.num_experiment = self.result_list[len(self.result_list)-1][0]
        #self.num_runs = self.result_list[len(self.result_list)-1][1]
        self.monte_trials = self.result_list[len(self.result_list)-1][1]
        self.theta_list = []
        self.delta_list = []


    def create_df(self):
        new_index  = []
        for i in self.index_range:
            new_index.append(i)
        self.df = pd.DataFrame(result_list, columns=["experiments", "runs", "theta", "delta", "outcome", "num_A"],
                          index=new_index)  # create dataframe
        return self.df

    def get_theta(self):
        for list in self.result_list:
            if ast.literal_eval(list[2]) not in self.theta_list:
                self.theta_list.append(ast.literal_eval(list[2]))
            else:
                pass
        return self.theta_list

    def get_delta(self):
        for list in self.result_list:
            if ast.literal_eval(list[3]) not in self.delta_list:
                self.delta_list.append(ast.literal_eval(list[3]))
            else:
                pass
        return self.delta_list

#get specifics from dataframe

df = DataFrame().create_df()

total_row = int(len(df.index))
num_experiment = DataFrame().num_experiment
num_monte_trials  = int(DataFrame().monte_trials)
print("\n", "num_experiment:",(int(num_experiment)+1), "\n", "num_monte_trials:",num_monte_trials)
#theta_list = DataFrame().get_theta()
num_runs = int(df["runs"][total_row])
delta_list = DataFrame().get_delta()
print("delta_list:",delta_list)
print("num_subjects/runs:", num_runs)



#set rules of holt_laury for CRRA coefficient
class Holt_Laury(object):
    def __init__(self):
        self.num_A = None

    def return_hit_num(self, theta):
        if -0.15 <= theta < 0.15:
            self.num_A = 4
        elif 0.15 <= theta < 0.41:
            self.num_A = 5
        elif 0.41 <= theta < 0.68:
            self.num_A = 6
        elif 0.68 <= theta < 0.97:
            self.num_A = 7
        elif 0.97 <= theta < 1.356:
            self.num_A = 8
        elif theta < -0.49:
            self.num_A = 2
        elif -0.49 <= theta < -0.15:
            self.num_A = 3
        return self.num_A

class Hit_Calculator(object):
    def __init__(self):
        self.hits = []
        self.numA_list = df["num_A"].tolist()
        self.theta_list = df["theta"].tolist()


        self.hit_rate  = None
        self.experiments_numA_list = []
        self.holt_laury_numA_list = []
        self.df2 = None
        self.theta  =[]
        self.hit_rate_list = []


    def hit_calc(self):

        if len(self.theta_list) == len(self.numA_list):
            for i in range(len(self.numA_list)):
                if Holt_Laury().return_hit_num(float(self.theta_list[i])) == self.numA_list[i]:
                    self.hits.append(1)
                else:
                    self.hits.append(0)
        return self.hits











hits_list = Hit_Calculator().hit_calc()
print(hits_list)

df["hits"] = hits_list
print(df)

df.to_csv("Holt_Laury_Output logit analysis1.csv")


"""    # pull from df the actual num_A from monte_carlo
    def monte_numA(self):
        temp_whole_list = df["num_A"].tolist()
        #print(temp_whole_list)
        temp_list = []
        temp_numA = []
        slice_range = total_row / (num_runs)
        df2_column = []

        for i in range(1, (int(num_experiment)+1+1)):
            df2_column.append("exp%d"%i)


        for i in range(int(slice_range)):
            temp_list = temp_whole_list[num_runs*i: num_runs*i+num_runs] #check here if it is always correct
            temp_numA.append(temp_list)
        #print(len(temp_numA))
        #print(temp_numA)

        for k in range(int(num_monte_trials)):
            temp_list  = temp_numA[(int(num_experiment)+1) * k: (int(num_experiment)+1) * k + int(num_experiment)+1]#check here if it is always correct
            self.experiments_numA_list.append(temp_list)

        df2 = pd.DataFrame(self.experiments_numA_list, columns=df2_column, index=["delta1","delta2","delta3","delta4"]) #if experiments number too large, create a list of strings that makes columns

        print("\n")
        print("A dataframe of numA in monte carlo")
        print(df2)
        print("\n")
        return df2

    def theta_list(self):
        temp_whole_list = df["theta"].tolist()
        print(temp_whole_list)
        temp_list = []
        temp_theta = []
        theta_list = []
        slice_range = total_row / (num_runs)

        for i in range(int(slice_range)):
            temp_list = temp_whole_list[4 * i: 4 * i + 4]
            temp_theta.append(temp_list)
        print(len(temp_theta))


        for k in range(int(num_monte_trials)):
            temp_list  = temp_theta[(int(num_experiment)+1) * k: (int(num_experiment)+1) * k + int(num_experiment)+1]
            theta_list.append(temp_list)
        return theta_list

"""
