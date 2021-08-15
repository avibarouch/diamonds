from flask import *
import numpy as np
import pandas as pd
import pickle


def area(x, y):
    return round(x*y*3.1415927/4, 3)


def form(x, y):
    return round((abs(x - y)/y*100), 3)


# Takes dictionaries from a list of them and merge them into a big one
def merge_dict_list(d_list):
    dic = {}
    for d in d_list:
        for val in d.keys():
            dic[val] = d[val]
    return dic


def original2model(in_dict, m_col_names, alpha_col, encode_dic):
    out_dict = {}
    for item in m_col_names:
        if item in alpha_col:
            out_dict[item] = encode_dic[in_dict[item]]
        else:
            if item in in_dict:
                out_dict[item] = in_dict[item]
            else:
                if item == "area":
                    out_dict[item] = area(in_dict["x"], in_dict["y"])
                if item == "form":
                    out_dict[item] = form(in_dict["x"], in_dict["y"])
    return out_dict


def diamond_price(in_dict):
    encode_dic = \
        {'Ideal': '1', 'Premium': '2', 'Very Good': '3', 'Good': '4',
         'Fair': '5', 'G': '1', 'E': '2', 'F': '3', 'H': '4', 'D': '5',
         'I': '6', 'J': '7', 'SI1': '1', 'VS2': '2', 'SI2': '3',
         'VS1': '4', 'VVS2': '5', 'VVS1': '6', 'IF': '7', 'I1': '8'}

    alpha_col = ['cut', 'color', 'clarity']

    m_col_names = ["carat", "cut", "color", "clarity", "z", "area"]

    out_dict = original2model(in_dict, m_col_names, alpha_col, encode_dic)

    vals = list(out_dict.values())
    keys = list(out_dict.keys())
    x_test = pd.DataFrame([vals], columns=keys)
    print(x_test)

    try:
        model = pickle.load(open("model_rf.pkl", "rb"))
        price = model.predict(x_test)
    except:
        flash("Sorry someting worong try again later")
    in_dict["price"] = int(price)
