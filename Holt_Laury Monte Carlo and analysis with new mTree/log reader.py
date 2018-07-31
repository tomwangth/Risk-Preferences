import csv
import itertools
import numpy as np

'''This is a log reader for output of Holt Laury simulation'''

with open("experiment.log") as in_file, open("HL.csv", "w") as out_file:
    writer = csv.writer(out_file)
    writer.writerow(["experiment", "run", "theta", "delta",  "choice1", "choice2","choice3","choice4","choice5","choice6","choice7","choice8","choice9","choice10","epsilon", "numA", "expected numA", "hits", "switch","cross_term"])

    for line in in_file:
        print(line.split(","))
        experiment = line.split()[4].split("([")[1].split(",")[0]
        print("exp:",experiment)
        run = line.split()[5].split(",")[0]
        print("run:",run)
        theta = line.split()[6].split(",")[0]
        print("theta:",theta)
        delta = line.split()[7].split(",")[0]
        print("delta:", delta)
        outcome = []
        for i in range(8,18):
            outcome_temp = line.split()[i].split(",")[0]
            #print((outcome_temp))
            outcome.append(outcome_temp)
            #outcome = outcome[0]

        choice1 = outcome[0][2:5]
        outcome_list = [choice1]
        for i in range(1,9):
            outcome_list.append(outcome[i][1:4])
        choice10 = outcome[9][1:5]
        outcome_list.append(choice10)
        print("outcome:", outcome_list)

        """count for numA"""

        numA = 0
        for choice in outcome_list:
            print(choice)
            if "A" in choice:
                numA += 1

        '''count for switches'''
        switch =0
        for i in range(9):
            print(outcome_list[i][0])
            if outcome_list[i][0] != outcome_list[i+1][0]:
                switch +=1

        def return_hit_num(theta):
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
            elif theta < -0.49:
                self.num_A = 2
            elif -0.49 <= theta < -0.15:
                num_A = 3
            return num_A

        expected_A = return_hit_num(float(theta))
        print("expected numA:", expected_A)
        hits = None
        if return_hit_num(float(theta)) == numA:
            hits = 1
        else:
            hits = 0
        print("numA:", numA)
        print("hits", hits)

        epsilon = line.split()[18].split("],")[0]
        print("epsilon:",epsilon)
        writer.writerow([experiment, run, theta, delta, outcome_list[0],outcome_list[1],outcome_list[2],outcome_list[3],outcome_list[4],outcome_list[5],outcome_list[6],outcome_list[7], outcome_list[8],outcome_list[9], epsilon, numA, expected_A, hits, switch,(float(epsilon)*float(delta))])


#TODO take a look at crossing pts numbers
#TODO find the percentage of predictions
#TODO find the border theta see if there is switches

