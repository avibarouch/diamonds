from flask import request, render_template
import json
import pandas as pd
import pickle

flag = 0
df = None


def init_df():
    global df, flag

    if flag == 0:
        flag = 1
        df = pd.read_csv('./data/diamond.csv').head(20)


def configure(app):

    @app.route('/')
    def hello_world():
        global df
        init_df()
        return render_template('main.html', data=df)

    @app.route('/addnew')
    def add_new():
        return render_template('addnew.html')

    @app.route('/predict')
    def predict():
        return render_template('predict.html')

    @app.route('/admin')
    def admin():
        return render_template('admin.html')

    @app.route('/details/<int:id>')
    def getdetails(id):
        global df
        return render_template('details.html', item=df.iloc[id])

    @app.route('/additem', methods=['POST'])
    def additem():
        global df
        carat = request.form['carat']
        cut = request.form['cut']
        color = request.form['color']
        clarity = request.form['clarity']
        depth = request.form['depth']
        x = request.form['x']
        y = request.form['y']
        z = request.form['z']
        price = request.form['price']
        df.loc[df.index.size] = [carat, cut, color, clarity,
                                 depth, x, y, z, price]
        # Data frame to CSV file
        df.to_csv('./data/diamond.csv', index=False)
        return render_template('ok.html')

    @app.route('/predict', methods=['POST'])
    def predictitem():
        global df
        carat = request.form['carat']
        cut = request.form['cut']
        color = request.form['color']
        clarity = request.form['clarity']
        depth = request.form['depth']
        x = request.form['x']
        y = request.form['y']
        z = request.form['z']

        # Open The model
        f = open('./data/modeldata', 'rb')
        model = pickle.load(f)
        f.close()

        ls = [carat, cut, color, clarity, depth, x, y, z]

        v = model.predict([ls])

        return render_template('res.html', val=v)
