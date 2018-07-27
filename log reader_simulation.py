import csv
import numpy as np
import ast
import pandas as pd

class log_reader(object):

    def __init__(self):
       self.data = []

    def DataFrame(self, file_name):
        in_file = open(file_name, "r")

        for line in in_file:
            newline = line[37:]
            dict = ast.literal_eval(newline)[0]
            agent_id = dict['agent_id']
            timestamp = dict['timestamp']
            round = dict['round_number']
            est_theta = dict['estimated_theta']
            treatment_set = dict['treatment_set']
            treatment = dict['treatment']
            B1_payoff = dict['b1_payoff']
            B1_prob = dict['b1_high_probability']
            B2_payoff = dict['b2_payoff']
            B2_prob = dict['b2_high_probability']
            B3_payoff = dict['b3_payoff']
            B3_prob = dict['b3_high_probability']
            order_1 = dict['Order_1']
            order_2 = dict['Order_2']
            order_3 = dict['Order_3']
            O1_success = dict['open_1_sucess']
            O1_stop = dict['open_1_stop']
            O2_success = dict['open_2_sucess']
            O2_stop = dict['open_1_stop']
            O3_success = dict['open_3_sucess']
            O3_stop = dict['open_1_stop']
            switch_point = dict['switching_point']
            selected_box = dict['selected_box']
            above_or_below = dict['above_or_below']
            selected_round_1 = dict['selected_round_1']
            selected_round_2 = dict['selected_round_2']
            payoff_normal = dict['payoff_normal']
            payoff_treatment = dict['payoff_treatment']
            total_payoff = dict['running_sum']
            delta = dict['delta']
            epsilon = dict['epsilon_sd']

            self.data.append([agent_id, timestamp, round, est_theta, treatment_set, treatment,
                              B1_payoff, B1_prob, B2_payoff, B2_prob, B3_payoff, B3_prob, order_1, order_2, order_3,
                              O1_success, O1_stop, O2_success, O2_stop, O3_success, O3_stop, switch_point,
                              selected_box, above_or_below, selected_round_1, selected_round_2,
                              payoff_normal, payoff_treatment, total_payoff, delta, epsilon])


        column = ["agent_id", "timestamp", "round",
                  "est_theta", "treatment_set", "treatment", "B1_payoff", "B1_prob", "B2__payoff",
                  "B2__prob", "B3_payoff", "B3_prob", "order_1", "order_2", "order_3",
                  "O1_success", "O1_stop", "O2_success", "O2_stop", "O3_success", "O3_stop",
                  "switch_point", "selected_box", "above_or_below","selected_round_1", "selected_round_2",
                  "payoff_normal", "payoff_treatment", "total_payoff", "delta", "epsilon"]
        df = pd.DataFrame(self.data, columns = column)
        return df

df1 = log_reader().DataFrame("Weitzman_experiment.log")
print(df1)

