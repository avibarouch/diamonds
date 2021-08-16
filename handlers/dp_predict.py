from flask import *
import numpy as np
import pandas as pd
import pickle


def area(x, y):
    if x == None or y == None:
        return None
    else:
        return round(x*y*3.1415927/4, 3)


def form(x, y):
    if x == None or y == None or y == 0:
        return None
    else:
        return round((abs(x - y)/y*100), 3)


# Takes dictionaries from a list of them and merge them into a big one
def merge_dict_list(d_list):
    dic = {}
    for d in d_list:
        for val in d.keys():
            dic[val] = d[val]
    return dic


def original2model(diamond, m_col_names, alpha_col, encode_dic):
    out_dict = {}
    for item in m_col_names:
        if item in alpha_col:
            if diamond[item]:
                out_dict[item] = encode_dic[diamond[item]]
            else:
                out_dict[item] = None
        else:
            if item in diamond:
                out_dict[item] = diamond[item]
            else:
                if item == "area":
                    if diamond["x"] and diamond["y"]:
                        out_dict[item] = area(diamond["x"], diamond["y"])
                    else:
                        out_dict[item] = None
                if item == "form":
                    if diamond["x"] and diamond["y"]:
                        out_dict[item] = form(diamond["x"], diamond["y"])
                    else:
                        out_dict[item] = None
    return out_dict


def diamond_price(diamond):
    encode_dic = \
        {'Ideal': '1', 'Premium': '2', 'Very Good': '3', 'Good': '4',
         'Fair': '5', 'G': '1', 'E': '2', 'F': '3', 'H': '4', 'D': '5',
         'I': '6', 'J': '7', 'SI1': '1', 'VS2': '2', 'SI2': '3',
         'VS1': '4', 'VVS2': '5', 'VVS1': '6', 'IF': '7', 'I1': '8'}

    alpha_col = ['cut', 'color', 'clarity']
    m_col_names = ["carat", "cut", "color", "clarity", "z", "area"]

    out_dict = original2model(diamond, m_col_names, alpha_col, encode_dic)

    vals = list(out_dict.values())
    keys = list(out_dict.keys())
    x_test = pd.DataFrame([vals], columns=keys)
    print(x_test)
    
    price = 0
    model_name = "model_rf.pkl"

    try:
        model = pickle.load(open("model_rf.pkl", "rb"))
    except:
        print(f"Unable to load {model_name} as a pickle file")
    else:
        try:
            price = model.predict(x_test)
        except:
            print(f"Unable to apply model {model_name}\non data:\n{x_test}\n obtained from user's data:\n {diamond}")
        else:
            return round(list(price)[0])
        finally:    
            diamond["price"] = 0
        
