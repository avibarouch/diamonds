import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression

from sklearn.model_selection import train_test_split
import sklearn.ensemble as ske

import sklearn.metrics as skme

import pickle


# Takes a vector, returns max string length and its index
def max_str(vec):
    maxLen = len(str(vec[0]))
    maxLenInd = 0
    for i in range(1, len(vec)):
        length = len(str(vec[i]))
        if length > maxLen:
            maxLen = length
            maxLenInd = i
    return (maxLenInd, maxLen)


# Takes a list and trims it to a given length, supplying given values
def complete_vec(vec, to_length, default=None):
    n = len(vec)
    if n <= to_length:
        for i in range(n, to_length):
            vec.append(default)
    return vec[:to_length]


def list2D1D(list2D):
    list1D = []
    for item in list2D:
        for val in item:
            list1D.append(val)
    return list1D


# Takes a list of dictionaries and returns
# a list of keys_lists and a list of values_lists
def keys_values(dicts_list):
    names = []
    values = []
    for item in dicts_list:        # every item is a dictionary!
        names.append(list(item.keys()))
        values.append(list(item.values()))
    return (names, values)


# Takes a dFrame and returns list of non-numerical columns (strings)
def non_num_col(dFrame):
    cols = list(dFrame.columns)
    non_num = []
    for i in range(len(cols)):
        if not dFrame[cols[i]].dtype.kind in 'biufc':
            non_num.append(cols[i])
    return non_num


# Takes dataFrame and conditions on values per columns and
# returns indexes of the rows (one may want to drop)
# 'col_names' should be validates against 'None' (not done yet)
def df_query(dFrame, col_names, ops=["=="],  thresh_vals=[0]):
    # input validation (col_names, ops,  thresh_vals)
    n_cols = len(col_names)
    n_ops = len(ops)
    n_thresh = len(thresh_vals)
    if (n_ops > n_cols) or (n_thresh > n_cols):
        return False
    if (n_ops < n_cols):
        for i in range(n_ops, 3):
            ops.append(ops[0])
    if (n_thresh < n_cols):
        for i in range(n_ops):
            thresh_vals[i] = thresh_vals[0]
    # conditions (separately for each columns):
    condition = []
    for i in range(n_cols):
        condition.append(col_names[i] + ops[i] + str(thresh_vals[i]))
    # assemblying the whole query:
    c_query = condition[0]
    for item in condition[1:]:
        c_query += " & " + item
    # df_cond contaions all the roes in dFrame according to the query:
    df_cond = dFrame.query(c_query)
    return list(df_cond.index)


# Takes dFrame and returns a the incidence of each value (%),
# for all columns - as a list of panda Series
def df_unique(dframe):
    n_rows = len(dframe)
    n_cols = len(dframe.columns)
    cols = list(dframe.columns)
    df_list = []
    for item in cols:
        df_list.append(round(dframe[item].value_counts()/n_rows*100))
    return df_list


# Takes a list of panda Series and returns it as a dictionary
def pdSeries2Dict(pdS):
    alpha = []  # each "alpha" member is a dictionary
    for item in pdS:
        dict = {}
        for i in range(len(item)):
            dict[item.keys()[i]] = item.array[i]
        alpha.append(dict)
    return alpha


# Produces 2 explanatory upper rows of a table (feature names and a delimiter)
# maxLen_vec's each list-member is the maximum string length on column
def table_title(feature_names, maxLen_vec, units=['%'], line_ch='-',
                space_len=5):
    if (type(feature_names) is not list or
            type(maxLen_vec) is not list or
            type(units) is not list):
        return ("List type was expected in function 'table_title'",
                "Nothing printed")
        if len(feature_name) < 1:
            feature_name.append("no_name")
        if len(maxLen_vec) < 1:
            maxLen_vec.append(30)
        if len(units) < 1:
            units.append(' ')
    row1 = ''
    row2 = ''
    n = len(feature_names)
    # If fixed-width columns prefered, than maxLen_vec = [constant]
    complete_vec(maxLen_vec, n, maxLen_vec[-1])
    complete_vec(units, n, units[-1])
    for i in range(len(feature_names)):
        data = feature_names[i] + units[i]
        dash_len = maxLen_vec[i]
        data_len = len(data)
        if dash_len < data_len:
            dash_len = data_len
        ad_space = (len(data) + 1) % 2
        before = int((dash_len - data_len)/2)
        after = dash_len - before - data_len
        row1 += ' '*before + data + ' '*(after + space_len)
        row2 += '-'*(dash_len) + ' '*space_len
    return (row1, row2)


# Produces a table of multiple dictionaries
# Uses function 'table_title'
def print_dictionaries(dicts_list, cols, separator=" : ",
                       units=['%'], line_ch='-', space_len=5):
    names, values = keys_values(dicts_list)
    n = len(dicts_list)
    # keys parameters used for print:
    max_strs = []
    max_strs_len = []
    n_of_unique_vals = []
    for item in names:
        max_strs.append(max(item))
        max_strs_len.append(len(max(item)))
        n_of_unique_vals.append(len(item))
    max_n_of_unique_vals = max(n_of_unique_vals)
    # values parameters used for print:
    max_value_length = []
    for vec in values:
        maxLenInd, maxLenVal = max_str(vec)
        max_value_length.append(maxLenVal)
    # dictionary-item parameters used for print:
    max_pair_length = []  # maximum length of a dictionary item, per feature
    for i in range(n):
        max_pair_length.append(len(max_strs[i]) +
                               len(separator) + max_value_length[i])
    (row1, row2) = table_title(cols, max_pair_length, units, line_ch,
                               space_len)
    print(f"{row1}\n{row2}")
    for row in range(max_n_of_unique_vals):
        for col in range(n):
            if row < len(names[col]):
                gap_str1 = ' '*(max_strs_len[col] - len(names[col][row]))
                gap_str2 = ' '*(max_value_length[col] -
                                len(str(values[col][row])))
                row_str = (names[col][row] + gap_str1 + separator +
                           gap_str2 + str(values[col][row]))
            else:
                row_str = ' '*max_pair_length[col]
            print(f"{row_str}{' '*space_len}", end='')
        print('')


# numerical encoding for non-numerical features (alpha_col) in dFrame:
def num_code(dFrame, alpha_col):
    alpha = pdSeries2Dict(df_unique(dFrame[alpha_col]))
    alpha_encode = []
    alpha_decode = []
    i = 0
    for dic in alpha:
        j = 1
        encode = {}
        decode = {}
        for item in dic:
            dFrame.loc[dFrame[alpha_col[i]] == item, alpha_col[i]] = j
            encode[item] = str(j)
            decode[str(j)] = item
            j += 1
        alpha_encode.append(encode)
        alpha_decode.append(decode)
        i += 1
    return (dFrame, alpha_encode, alpha_decode)


# Finding missing values (after finding "bad" values)
def missing_per_column(dFrame):
    dictio = {}
    for item in dFrame.columns:
        null_per_column = dFrame[item].isnull().sum()
        dictio[item] = null_per_column
    return dictio


# Finding regression columns and columns to be repaired
# max_num is the maximum number of missing cells/column accepted
# All the rows containing less than max_num missing cells,
# are considered "safe" to delete
def separate_cols(dic, max_num):
    cols_del_rows = []
    cols_to_repair = []
    cols_full = []
    for k, v in dic.items():
        if v > 0 and v < max_num:
            cols_del_rows.append(k)
        if v >= max_num:
            cols_to_repair.append(k)
        if v == 0:
            cols_full.append(k)
    return (cols_del_rows, cols_to_repair, cols_full)


# Very specific to project "diamonds" function
# Input:  dFrame after initial cleaning
# Output: dFrame ("x", "y") >>> ("area", "form")
def area(x, y):
    return round(x*y*3.1415927/4, 3)


def form(x, y):
    return round((abs(x - y)/y*100), 3)


def diamond_xy(df):
    df["area"] = round(df["x"]*df["y"]*3.1415927/4, 3)
    df["form"] = round((abs(df["x"] - df["y"])/df["y"]*100), 3)
    return df.drop(["x", "y"], axis=1)


# repair_col may be applied to any numerical column with ~0 values, in df_name
def repair_col(df_name, col_name, min_cond, dec_num_precision):
    df_name.loc[df_name[col_name] is not None and
                df_name[col_name] < min_cond, col_name] = None
    train_data = df_name[df_name[col_name].isnull() is False]
    test_data = df_name[df_name[col_name].isnull() is True]
    x_train = train_data.drop([col_name], axis=1)
    y_train = train_data[col_name]
    x_test = test_data.drop([col_name], axis=1)
    lr = LinearRegression()
    lr.fit(x_train, y_train)
    predict_col = lr.predict(x_test)
    test_complete = x_test.copy()
    test_complete[col_name] = list(map(lambda x: round(x, dec_num_precision),
                                       predict_col))
    return pd.concat([train_data, test_complete], axis=0)


# Takes a dFrame and a target column-name and produces a list of
# column names which don't correlate well (min_val) with the target
def corr_drop(d_f, column_name, min_val=0.1, method="Pearson"):
    corr_col = abs(d_f.corr()[column_name])
    drop_vec = []
    for i in range(len(corr_col)):
        if(corr_col[i] < min_val):
            drop_vec.append(d_f.corr().columns[i])
    return drop_vec


# Takes a dFrame, a feature string and a dict and returns indexes of rows in
# the dFrame where the feature's value doesn't obey the condition set below.
# "feature" should be a numerical features. USED BY "weird_rows" FUNCTION!
def append_weird_rows(df_name, feature, sig_num=6):
    dictionary = {}
    # Ridiculous (high) > Mean + ()*Sigma
    ridicul_pos = df_name[feature].mean() + sig_num*df_name[feature].std()
    # Ridiculous (high) > Mean + ()*Sigma
    ridicul_neg = df_name[feature].mean() - sig_num*df_name[feature].std()
    if ridicul_neg < 0:
        ridicul_neg = 0
    condition = feature + " > " + str(ridicul_pos) + " or " + \
        feature + " < " + str(ridicul_neg)
    weird_df = df_name.query(condition)
    rows = list(weird_df.index)
    for i in range(len(rows)):
        dictionary[(feature, round(ridicul_pos, 3),
                    round(ridicul_neg, 3), i)] = rows[i]
    return dictionary


# Finds unique indexes of all weird_rows in the dFrame given.
# "df_frame" should comprise only of numerical features.
# Returns the indexes of those rows in df_name, as a list
def weird_rows(df_name, alpha, sig_num=6):
    d = {}
    for i in range(len(df_name.columns)):
        feature = df_name.columns[i]
        if feature not in alpha:
            d.update(append_weird_rows(df_name, feature, sig_num))
    return d


# Finds all the indexes in dFrame on columns 'cols' where'ch' strings occurs
def string_index_in_df(df, cols, ch):
    index = []
    for col in df[cols]:
        i = 0
        for item in df[col]:
            i += 1
            if item == ch:
                index.append(i)
    return index


# Produces a RF_model for predicting "col_name" in "df_name"
def rf(df_name, col_name, mytest_size=0.2):
    X = df_name.drop([col_name], axis=1)
    y = df_name[col_name]
    x_train, x_test, y_train, y_test = \
        train_test_split(X, y, test_size=mytest_size, random_state=66)
    model = ske.RandomForestRegressor()
    model.fit(x_train, y_train)
    return (model, x_test, y_test)


# Check accuracy (for those who don't trust the "sklearn.metrics")
def myR2(y_test, y_pred):
    sum = 0
    n = len(y_test)
    for i in range(n):
        sum += (1 - y_pred[i]/y_test[i])**2
    sqrt_sum = (sum/n)**0.5
    return 1 - sqrt_sum


# Returns various accuracy metrics for "test" and "predict" data
def print_scores(x_test, y_test, y_predict):
    score_model = model_rf.score(x_test, y_test)
    mse = skme.mean_squared_error(y_test, y_predict)
    mae = skme.mean_absolute_error(y_test, y_predict)
    rmse = skme.mean_squared_error(y_test, y_predict)**0.5
    my_r2 = myR2(np.array(y_test), y_predict)
    r2 = skme.r2_score(y_test, y_predict)
    MaxAE = max(y_predict) - max(y_test)
    MinAE = min(y_predict) - min(y_test)
    print('score  : %0.4f ' % score_model)
    print('MSE    : %0.2f ' % mse)
    print('MAE    : %0.2f ' % mae)
    print('RMSE   : %0.2f ' % rmse)
    print('myR2   : %0.2f ' % my_r2)
    print('R2     : %0.2f ' % r2)
    print('MaxAE  : %0.2f ' % MaxAE)
    print('MinAE  : %0.2f ' % MinAE)
    return score_model


def make_pickle(model_name, pickle_name, path):
    with open(path + pickle_name, 'wb') as f:
        pickle.dump(model_name, f)


##################################################################
# ################# Start of data preparation ################## #
##################################################################

# Original data-base:
df = pd.read_csv("data/diamond.csv")
df = df.drop('Unnamed: 0', axis=1)

# Finding non-numerical feature (list):
alpha_col = non_num_col(df)

# Replaces all space only or special charater values with NaN
df.replace(r'^\s*$', np.nan, regex=True)

# Finding unwanted rows (beyond repair, known condition):
# (Specific to project)
z00_indexes = []
z00_indexes.append(df_query(df, ["x", "y"], ["<"],  [0.1, 0.1]))
z00_indexes.append(df_query(df, ["y", "z"], ["<"],  [0.1, 0.1]))
z00_indexes.append(df_query(df, ["z", "x"], ["<"],  [0.1, 0.1]))
z00_indexes = set(list2D1D(z00_indexes))

# Cleaning 'z00' unwanted rows:
df1 = df.drop(axis=0, index=z00_indexes)

# Convert non-numerical columns (alpha_col) to numeric
# 'alpha_encode' and 'alpha_decode' are translation dictionaries
(df2, alpha_encode, alpha_decode) = num_code(df1, alpha_col)

# Replacing all spaces and special characters in df2 - with NaN:
df3 = df2.replace(r'^\s*$', np.nan, regex=True)

# Finds number of missing cells in each column (dFrame - alternative example)
dic = missing_per_column(df2)

# All these lists of columns are used in finding missing values:
cols_del_rows, cols_to_repair, cols_full = separate_cols(dic, 3)
# print(f"In columns: {cols_del_rows} delete rows having missing values")
# print(f"Columns to complete: {cols_to_repair}")
# print(f"Full columns: {cols_full}")

# Drop rows in 'cols_del_rows' having None or NaN values
df3 = df2.dropna(axis=1, subset=cols_del_rows)

# Repair columns with missing or wrong value:
for col in cols_to_repair:
    df3 = repair_col(df3, col, min_cond=0.1, dec_num_precision=3)

# Find (weird) rows with far-off values (n*std)
d_weird_rows = weird_rows(df3, alpha_col, sig_num=6)
weird_indexes = set(d_weird_rows.values())

# Cleaning weird_rows:
df4 = df3.drop(axis=0, index=weird_indexes)
print(f"How much we drop: {len(weird_indexes)}/{len(df3)}")

# Changing 'x', 'y' columns to 'area', 'form'
# (Specific to project)
df5 = diamond_xy(df4)

# Dropping columns which have little corelation with the price
drop_col = corr_drop(df5, "price", 0.5)
# print(drop_col)   # 0.2 to 0.8 : ['depth', 'table', 'form']
df6 = df5.drop(drop_col, axis=1)

##################################################################
# ################## End of data preparation ################### #
##################################################################

# Applying a machine learning model for "price" column:
model_rf, x_test, y_test = rf(df6, "price", mytest_size=0.15)
# y_predict = model_rf.predict(x_test)
# print_scores(x_test, y_test, y_predict)

# Makes pickle file (model_rf.pkl):
make_pickle(model_rf, "model_rf.pkl", "")
