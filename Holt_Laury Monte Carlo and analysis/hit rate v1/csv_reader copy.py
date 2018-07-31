import csv
import ast
import pandas as pd
import re
import sympy as sp

# create a class to read csv and store things in a dict
theta1 = {"theta": 0.2, "outcome":[]}
theta2 = {"theta": 0.4, "outcome":[]}
theta3 = {"theta": 0.6, "outcome":[]}
theta4 = {"theta": 0.8, "outcome":[]}
temp_t1 = []
temp_t2 = []
temp_t3 = []
temp_t4 = []

with open("Holt_Laury_Output.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        #print(row)

        if row[2] == "0.2":
            temp_t1 = [float(row[3]),ast.literal_eval(row[4])]
            #print(temp_t1)
            theta1["outcome"].append(temp_t1)
        else:
            pass

        if row[2] == "0.4":
            temp_t2 = [float(row[3]),ast.literal_eval(row[4])]
            theta2["outcome"].append(temp_t2)
        else:
            pass

        if row[2] == "0.6":
            temp_t3 = [float(row[3]),ast.literal_eval(row[4])]
            theta3["outcome"].append(temp_t3)
        else:
            pass

        if row[2] == "0.8":
            temp_t4 = [float(row[3]),ast.literal_eval(row[4])]
            theta4["outcome"].append(temp_t4)
        else:
            pass

    print(theta1)
    print(theta2)
    print(theta3)
    print(theta4)
    result_list1 = (theta1, theta2, theta3, theta4)
    print(result_list1)




#create a class to calculate hit rate
class HitRate(object):
    def __init__(self):
        self.num_A = None
        self.hit = 0
        self.failure = 0
        self.total_run = 0

        self.numA_sd1 = 0
        self.numA_sd2 = 0
        self.numA_sd3 = 0
        self.numA_sd4 = 0

    # set up the right holt-laury lottery theta value, get hit rate
    def eval_hit(self, theta, num_A):

        hit = 0
        if -0.15 <= theta < 0.15:
            if num_A == 4:
                hit += 1

        elif 0.15 <= theta < 0.41:
            if num_A == 5:
                hit += 1

        elif 0.41 <= theta < 0.68:
            if num_A == 6:
                hit += 1

        elif 0.68 <= theta < 0.97:
            if num_A == 7 :
                hit += 1
        elif 0.97 <= theta < 1.356:
            if num_A == 8:
                hit += 1
        return hit

    def run_data(self, result_list):

        data = {}
        for i in range(4):
            data["theta%d" % i] = {}
            for outcome in result_list[i]["outcome"]:
                sd = outcome[0]
                for choice in outcome[1]:
                    if "A" in choice:
                        if sd == 0.1:
                            self.numA_sd1 += 1
                        elif sd == 0.2:
                            self.numA_sd2 +=1
                        elif sd == 0.3:
                            self.numA_sd3 +=1
                        elif sd == 0.4:
                            self.numA_sd4 +=1
                    data["theta%d" % i].update({"sd1" : self.numA_sd1, "sd2": self.numA_sd2, "sd3": self.numA_sd3, "sd4": self.numA_sd4})

            self.numA_sd1 = 0
            self.numA_sd2 = 0
            self.numA_sd3 = 0
            self.numA_sd4 = 0
        return data

print(HitRate().run_data(result_list1))



#def return hit rate, grab each item in the run_data list and run it with eval_hit


"""
        for round in range(len(row[4])):

            if "0.2" in round:
                theta1["%d" % float(round)] = round[round]

            if "0.4" in row:
                theta2.update({"%d" % float(round): row[4]})

            if "0.6" in row:
                theta3.update({"%d" % float(round): row[4]})
            if "0.8" in row:
                theta4.update({"%d" % float(round): row[4]})
    print(theta1, "\n")
    print(theta2, "\n")
    print(theta3, "\n")
    print(theta4, "\n")

def eval_hit(theta, num_A):
    hit = 0
    if -0.15 <= theta < 0.15:
        if num_A == 4:
            hit += 1

    elif 0.15 <= theta < 0.41:
        if num_A == 5:
            hit += 1

    elif 0.41 <= theta < 0.68:
        if num_A == 6:
            hit += 1

    elif 0.68 <= theta < 0.97:
        if num_A == 7:
            hit += 1
    elif 0.97 <= theta < 1.356:
        if num_A == 8:
            hit += 1
    return hit


a = []
for key, value in data.items():
    theta = 0.2
    for key2, value2 in value.items():
        for item in value2:

            a.append(item)
            eval_hit(theta, item)
    print(eval_hit(theta, item))
    theta += 0.2


#create a class to calculate hit rate

#plot it




# "Holt_Laury_Output.csv"
def _reader(file_name):
    '''readers csv and returns a dict. of outcome'''

    list_of_periods_raw = []  # empty list to store all of our periods
    with open(file_name) as f:
        reader = csv.reader(f)
        for r in reader:
            list_of_periods_raw.append(ast.literal_eval(r[1]))  # turns our string to dicts

    return list_of_periods_raw  # return all of the periods as a list of dicts


def _split_choices(raw_data):
    '''given the raw data, returns a dict with individual rows'''

    row_choice = {}  # store our choice for each row

    for i in range(len(raw_data["outcome"])):
        row_choice["Row_%d" % (i + 1)] = raw_data['outcome'][i][2][0]  # creates the row/choice pairing

    return row_choice  # return dict


def _format_cols(cols):  # returns a column with/ human sorted columns

    def atoi(text):  # ASCII to integer
        if text.isdigit():
            return int(text)
        else:
            return text

    def natural_keys(text):
        ans = []
        for c in re.split('(\d+)', text):
            ans.append(atoi(c))
        return ans

    cols.sort(key=natural_keys)
    return cols


def create_dataframe(file_name):
    '''
        Input:
            file_name(string): file name (ex. "Holt_Laury_Output.csv")

        Output:
            dataframe(df.DataFrame): data frame of all periods


    '''
    list_of_periods_raw = _reader(file_name)

    # a table stores the information about each period

    all_periods = []  # a list of tables for each period to be used in df

    for curr_raw_period in list_of_periods_raw:

        period = {}  # dict to store info on current period

        # set the period, theta and the sd for each table
        period["Period"] = curr_raw_period["Period"]
        period["theta"] = curr_raw_period["theta"]
        period["sd"] = curr_raw_period["sd"]

        # creates a dictionary w/ row as key and choice as val
        dict_of_choices = _split_choices(curr_raw_period)
        # add each row and choice to our table
        for key in dict_of_choices:
            period["%s" % key] = dict_of_choices[key]

        all_periods.append(period)  # appends the current table to a list of all tables

    # create dataframe
    df = pd.DataFrame(all_periods)

    # making sure columns are in the correct order
    cols = df.columns.tolist()

    # remove any of the none row_# columns
    cols.remove("sd")
    cols.remove("theta")
    cols.remove("Period")

    # natural sort the columns
    cols = _format_cols(cols)
    cols = ["Period", "theta", "sd"] + cols
    df = df[cols]

    #
    df.set_index("Period", inplace=True)
    return df

print(create_dataframe("Holt_Laury_Output.csv"))
"""









#plot it


"""
        for round in range(len(row[4])):

            if "0.2" in round:
                theta1["%d" % float(round)] = round[round]

            if "0.4" in row:
                theta2.update({"%d" % float(round): row[4]})

            if "0.6" in row:
                theta3.update({"%d" % float(round): row[4]})
            if "0.8" in row:
                theta4.update({"%d" % float(round): row[4]})
    print(theta1, "\n")
    print(theta2, "\n")
    print(theta3, "\n")
    print(theta4, "\n")


#create a class to calculate hit rate

#plot it
"""

"""
# "Holt_Laury_Output.csv"
def _reader(file_name):
    '''readers csv and returns a dict. of outcome'''

    list_of_periods_raw = []  # empty list to store all of our periods
    with open(file_name) as f:
        reader = csv.reader(f)
        for r in reader:
            list_of_periods_raw.append(ast.literal_eval(r[1]))  # turns our string to dicts

    return list_of_periods_raw  # return all of the periods as a list of dicts


def _split_choices(raw_data):
    '''given the raw data, returns a dict with individual rows'''

    row_choice = {}  # store our choice for each row

    for i in range(len(raw_data["outcome"])):
        row_choice["Row_%d" % (i + 1)] = raw_data['outcome'][i][2][0]  # creates the row/choice pairing

    return row_choice  # return dict


def _format_cols(cols):  # returns a column with/ human sorted columns

    def atoi(text):  # ASCII to integer
        if text.isdigit():
            return int(text)
        else:
            return text

    def natural_keys(text):
        ans = []
        for c in re.split('(\d+)', text):
            ans.append(atoi(c))
        return ans

    cols.sort(key=natural_keys)
    return cols


def create_dataframe(file_name):
    '''
        Input:
            file_name(string): file name (ex. "Holt_Laury_Output.csv")

        Output:
            dataframe(df.DataFrame): data frame of all periods


    '''
    list_of_periods_raw = _reader(file_name)

    # a table stores the information about each period

    all_periods = []  # a list of tables for each period to be used in df

    for curr_raw_period in list_of_periods_raw:

        period = {}  # dict to store info on current period

        # set the period, theta and the sd for each table
        period["Period"] = curr_raw_period["Period"]
        period["theta"] = curr_raw_period["theta"]
        period["sd"] = curr_raw_period["sd"]

        # creates a dictionary w/ row as key and choice as val
        dict_of_choices = _split_choices(curr_raw_period)
        # add each row and choice to our table
        for key in dict_of_choices:
            period["%s" % key] = dict_of_choices[key]

        all_periods.append(period)  # appends the current table to a list of all tables

    # create dataframe
    df = pd.DataFrame(all_periods)

    # making sure columns are in the correct order
    cols = df.columns.tolist()

    # remove any of the none row_# columns
    cols.remove("sd")
    cols.remove("theta")
    cols.remove("Period")

    # natural sort the columns
    cols = _format_cols(cols)
    cols = ["Period", "theta", "sd"] + cols
    df = df[cols]

    #
    df.set_index("Period", inplace=True)
    return df

print(create_dataframe("Holt_Laury_Output.csv"))



#create a class to calculate hit rate
class HitRate(object):
    def __init__(self):
        self.num_A = None
        self.hit = 0
        self.failure = 0
        self.total_run = 0

        self.numA_sd1 = 0
        self.numA_sd2 = 0
        self.numA_sd3 = 0
        self.numA_sd4 = 0

    # set up the right holt-laury lottery theta value, get hit rate


    def run_data(self, result_list):

        data = {}
        for i in range(4):
            data["theta%d" % i] = {}
            for outcome in result_list[i]["outcome"]:
                sd = outcome[0]
                for choice in outcome[1]:
                    if "A" in choice:
                        if sd == 0.1:
                            self.numA_sd1 += 1
                        elif sd == 0.2:
                            self.numA_sd2 +=1
                        elif sd == 0.3:
                            self.numA_sd3 +=1
                        elif sd == 0.4:
                            self.numA_sd4 +=1
                    data["theta%d" % i].update({"sd1" : self.numA_sd1, "sd2": self.numA_sd2, "sd3": self.numA_sd3, "sd4": self.numA_sd4})

            self.numA_sd1 = 0
            self.numA_sd2 = 0
            self.numA_sd3 = 0
            self.numA_sd4 = 0
        return data

#print(HitRate().run_data(result_list1))

"""
"""
        for round in range(len(row[4])):

            if "0.2" in round:
                theta1["%d" % float(round)] = round[round]

            if "0.4" in row:
                theta2.update({"%d" % float(round): row[4]})

            if "0.6" in row:
                theta3.update({"%d" % float(round): row[4]})
            if "0.8" in row:
                theta4.update({"%d" % float(round): row[4]})
    print(theta1, "\n")
    print(theta2, "\n")
    print(theta3, "\n")
    print(theta4, "\n")

def eval_hit(theta, num_A):
    hit = 0
    if -0.15 <= theta < 0.15:
        if num_A == 4:
            hit += 1

    elif 0.15 <= theta < 0.41:
        if num_A == 5:
            hit += 1

    elif 0.41 <= theta < 0.68:
        if num_A == 6:
            hit += 1

    elif 0.68 <= theta < 0.97:
        if num_A == 7:
            hit += 1
    elif 0.97 <= theta < 1.356:
        if num_A == 8:
            hit += 1
    return hit


a = []
for key, value in data.items():
    theta = 0.2
    for key2, value2 in value.items():
        for item in value2:

            a.append(item)
            eval_hit(theta, item)
    print(eval_hit(theta, item))
    theta += 0.2


#create a class to calculate hit rate

#plot it




# "Holt_Laury_Output.csv"
def _reader(file_name):
    '''readers csv and returns a dict. of outcome'''

    list_of_periods_raw = []  # empty list to store all of our periods
    with open(file_name) as f:
        reader = csv.reader(f)
        for r in reader:
            list_of_periods_raw.append(ast.literal_eval(r[1]))  # turns our string to dicts

    return list_of_periods_raw  # return all of the periods as a list of dicts


def _split_choices(raw_data):
    '''given the raw data, returns a dict with individual rows'''

    row_choice = {}  # store our choice for each row

    for i in range(len(raw_data["outcome"])):
        row_choice["Row_%d" % (i + 1)] = raw_data['outcome'][i][2][0]  # creates the row/choice pairing

    return row_choice  # return dict


def _format_cols(cols):  # returns a column with/ human sorted columns

    def atoi(text):  # ASCII to integer
        if text.isdigit():
            return int(text)
        else:
            return text

    def natural_keys(text):
        ans = []
        for c in re.split('(\d+)', text):
            ans.append(atoi(c))
        return ans

    cols.sort(key=natural_keys)
    return cols


def create_dataframe(file_name):
    '''
        Input:
            file_name(string): file name (ex. "Holt_Laury_Output.csv")

        Output:
            dataframe(df.DataFrame): data frame of all periods


    '''
    list_of_periods_raw = _reader(file_name)

    # a table stores the information about each period

    all_periods = []  # a list of tables for each period to be used in df

    for curr_raw_period in list_of_periods_raw:

        period = {}  # dict to store info on current period

        # set the period, theta and the sd for each table
        period["Period"] = curr_raw_period["Period"]
        period["theta"] = curr_raw_period["theta"]
        period["sd"] = curr_raw_period["sd"]

        # creates a dictionary w/ row as key and choice as val
        dict_of_choices = _split_choices(curr_raw_period)
        # add each row and choice to our table
        for key in dict_of_choices:
            period["%s" % key] = dict_of_choices[key]

        all_periods.append(period)  # appends the current table to a list of all tables

    # create dataframe
    df = pd.DataFrame(all_periods)

    # making sure columns are in the correct order
    cols = df.columns.tolist()

    # remove any of the none row_# columns
    cols.remove("sd")
    cols.remove("theta")
    cols.remove("Period")

    # natural sort the columns
    cols = _format_cols(cols)
    cols = ["Period", "theta", "sd"] + cols
    df = df[cols]

    #
    df.set_index("Period", inplace=True)
    return df

print(create_dataframe("Holt_Laury_Output.csv"))
"""