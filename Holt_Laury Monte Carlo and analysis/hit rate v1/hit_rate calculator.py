import csv
import ast
import pandas as pd
import re
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

#read csv and store things in a dict
theta_list = [0.2, 0.4, 0.6, 0.8]
sd_list = [0.1,0.2,0.3,0.4]
theta1 = {"theta": 0.2, "outcome":[]}
theta2 = {"theta": 0.4, "outcome":[]}
theta3 = {"theta": 0.6, "outcome":[]}
theta4 = {"theta": 0.8, "outcome":[]}
temp_t1 = []
temp_t2 = []
temp_t3 = []
temp_t4 = [] #temp_t store the theta temporarily for appending
new_list = []
temp_list = []
num_A = 0


with open("Holt_Laury_Output.csv") as f:
    reader = csv.reader(f)
    for row in reader:

        #print(row)
        temp_list = row

        for item in ast.literal_eval(row[4]):

            if "A" in item:
                num_A +=1

        temp_list.append(num_A)
        num_A = 0
        new_list.append(temp_list)





        if row[2] == "0.2":
            temp_t1 = [float(row[3]),ast.literal_eval(row[4]),temp_list[5]]
            #print(temp_t1)
            theta1["outcome"].append(temp_t1)
        else:
            pass

        if row[2] == "0.4":
            temp_t2 = [float(row[3]),ast.literal_eval(row[4]),temp_list[5]]
            theta2["outcome"].append(temp_t2)
        else:
            pass

        if row[2] == "0.6":
            temp_t3 = [float(row[3]),ast.literal_eval(row[4]), temp_list[5]]
            theta3["outcome"].append(temp_t3)
        else:
            pass

        if row[2] == "0.8":
            temp_t4 = [float(row[3]),ast.literal_eval(row[4]), temp_list[5]]
            theta4["outcome"].append(temp_t4)
        else:
            pass

    result_list1 = (theta1, theta2, theta3, theta4)
    print("result_list:", result_list1)

print("new_list:", new_list)
total_row =  len(new_list)


range1 = range(1,total_row+1) # rearrange index of df
new_index = []
for i in range1:
    new_index.append(i)
df = pd.DataFrame(new_list, columns = ["period","round","theta","sd","outcome","num_A"], index= new_index) #create dataframe
print(df)





# evaluate num_A given theta value

def holt_laury(theta):
    num_A = None
    if -0.15 <= theta < 0.15:
        num_A = 4

    elif 0.15 <= theta < 0.41:
        num_A = 5

    elif 0.41 <= theta < 0.68:
        num_A = 6

    elif 0.68 <= theta < 0.97:
        num_A = 7

    elif 0.97 <= theta < 1.356:
        num_A = 8

    return num_A

list_numA = [] #show that in holt-laury what should be num of A
for theta in theta_list:
    list_numA.append(holt_laury(theta))
print("list_numA w/ thetas:", list_numA)


list= []
data = {}

for i in range(4):
    data["theta%d" % (i+1)] = {}
    for thing in result_list1[i]["outcome"]:
        sd = thing[0]
        theta = result_list1[i]["theta"]
        list.append(thing[2])
        #if sd == 0.1:
            #list_1.append(thing[2])

        #if sd == 0.2:
            #list_2.append(thing[2])

            #print(list_2)

        #if sd == 0.3:
            #list_3.append(thing[2])
            #list_3 = list_3[20:29]

        #if sd == 0.4:
            #list_4.append(thing[2])
            #list_4 = list_4[30:39]

        #data["theta%d" % (i+1)].update({"sd1": list_1, "sd2": list_2, "sd3": list_3, "sd4": list_4})

print("whole list numA",list)
print(len(list))

list_1= list[0:40]
list_2 =list[40:80]
list_3 =list[80:120]
list_4 =list[120:160]
all_lists = [list_1, list_2, list_3, list_4]
data = {}

for i in range(4):
    data["theta %d" % (i+1)] = {}
print(data)



temp = []
temp2 = []
for list in all_lists:
    for i in range(4):
        temp = list[i*10 : i*10+10]
        print(temp)
        temp2.append(temp)

print(temp2)
temp3 = []
for i in range(0,16,4):
    temp3.append(temp2[i:i+4])
print(temp3)

for i in range(4):
    for k in range(4):
        data["theta %d" % (i + 1)]["sd%d" % (k + 1)] = temp3[i][k]
print(data)

#def return hit rate, grab each item in the run_data list and run it with eval_hit

def get_hit_rate(numA, data_set):

    hit = 0
    temp_list_hit = []
    list_hit = []

    for key, value in data_set.items():
            #print(value2)
            for item in value:
                if item == numA:
                    hit += 1

            list_hit.append([hit])
            hit = 0


    return list_hit

#get hit number for all theta and sd values

list_for_plot = []
for i in range(4):
    print(get_hit_rate(list_numA[i], data["theta %d" % (i+1)]))
    list_for_plot.append(get_hit_rate(list_numA[i], data["theta %d" % (i+1)]))
print(list_for_plot)


#plot hit rate

y=[]
pre_y = ()

for i in range(4):
    for k in range(4):
        pre_y += tuple(list_for_plot[k][i])
    y.append(pre_y)
    pre_y  = ()

print(y)

x = sd_list

for xe, ye in zip(x, y):
    plt.scatter([xe] * len(ye), ye)

plt.xticks([0.1, 0.2, 0.3, 0.4])
#plt.axes().set_xticklabels(['cat1', 'cat2'])

plt.savefig('t.png')


