from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import sklearn.ensemble as ske
import numpy as np
import pandas as pd

import pickle


df = pd.read_csv("/content/diamonds.csv")
# drop column 'Unnamed'
df1 = df.drop(df.columns[0], axis=1)

# Decided to drop rows where at least 2 of the [x,y,z] values are 0:
non_zero = ["carat", "depth", "table", "price", "x", "y", "z"]
start = non_zero.index("x")
df000 = df1.query("(x < 0.1) & (y < 0.1) & (z < 0.1)")
for i in range(3):
    first, second, third = start + i, start + (i+1) % 3, start + (i+2) % 3
    df00 = df1.query("({} < 0.1) & ({} < 0.1) & not({} < 0.1)".format(non_zero[first], non_zero[second], non_zero[third]))
    df000 = pd.concat([df000, df00])
df3 = df1.drop(axis=0, index=df000.index)

# Non numerical data:
alpha_cols = ["cut", "color", "clarity"]
df4 = df3[alpha_cols].copy()


# Find which columns better correlate with the partial missing "z" column:
def corr_drop(d_f, column_name, min_val=0.1, method="Pearson"):
    corr_col = abs(d_f.corr()[column_name])
    drop_vec = []
    for i in range(len(corr_col)):
        if(corr_col[i] < min_val):
            drop_vec.append(d_f.corr().columns[i])
    return drop_vec


# Drop columns who don't correlate with z:
drop_col = corr_drop(df3, "z", 0.3)
df30 = df3.drop(drop_col, axis=1)


# Using regression to predict the values of the 'z' column (where 0):

df30.loc[df['z'] < 0.1, 'z'] = None           # for z = 0 values are erased

train_data = df30[df30.z.isnull() == False]    # rows with full values
test_data = df30[df30["z"].isnull() == True]   # rows with no z values

train_num = train_data.drop(alpha_cols, axis=1)  # drop categorical
test_num = test_data.drop(alpha_cols, axis=1)    # drop categorical

y_train = train_num["z"]
train = train_num.drop("z", axis=1)
test = test_num.drop("z", axis=1)

# Using a linear regression model to predict z:

lr = LinearRegression()
lr.fit(train, y_train)

# Replace the empty 'z' values with the regression solution:
prediction = lr.predict(test)
test["z"] = prediction

# Reconstituting the table:
train_test = pd.concat([train_num, test])
df3["z"] = train_test["z"]

# Replacing columns 'x', 'y' with meaningful measures (area, form_coef):
df5 = df3.copy()
df5["xy"] = df3["x"]*df3["y"]*3.1415927/4   # max section area
deform = abs(round((df5["x"]-df5["y"])/df5["y"]*100, 3))
df5["form"] = deform                        # x = y --> form = 0 (%)
df5.drop(["x", "y"], axis=1, inplace=True)

# Adding back the "drop_col" columns:
# df5 = pd.concat([df5, df4], axis=1, join="inner")
# https://www.aqua-calc.com/calculate/weight-to-volume
# Make categoric data - numeric (get_dummy, fit_transform):

label_cut = LabelEncoder()
label_color = LabelEncoder()
label_clarity = LabelEncoder()
df50 = df5.copy()
df5['cut'] = label_cut.fit_transform(df3['cut'])
df5['color'] = label_color.fit_transform(df3['color'])
df5['clarity'] = label_clarity.fit_transform(df3['clarity'])

# Drop features who don't correlate with the price:
threshold = 0.03
drop_col = corr_drop(df5, "price", threshold)

# Split columns to be predicted, from the rest of the table:
X = df5.drop(['price'], axis=1)
y = df5['price']

# Split rows between train and test sections:

X_train, X_test, y_train,
y_test = train_test_split(X, y, test_size=0.2, random_state=66)

# Random Forest Method ('price', Regression)

model_rf = ske.RandomForestRegressor()
model_rf.fit(X, y)
y_pred = model_rf.predict(X_test)

# Export model to pickle format as 'modeldata.ext':

with open('modeldata', 'wb') as f:
    pickle.dump(model_rf, f)
