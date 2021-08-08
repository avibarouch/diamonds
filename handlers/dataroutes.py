import database.dp_db_insert
from flask import request, render_template
import json
import pandas as pd
import pickle
import handlers.buildmodel
# import database.dp_db_install
import dp_db_install
# import database.dp_db_connectivity_check
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
        print("Hello from predict_item on dataroutes.py")
        return render_template('details.html', item=df.iloc[id])

    @app.route('/additem', methods=['POST'])
    def add_item():
        global df
        print("Hello from add_item on dataroutes.py")
        carat = request.form['carat']
        cut = request.form['cut']
        color = request.form['color']
        clarity = request.form['clarity']
        depth = float(request.form['depth'])
        x = float(request.form['x'])
        y = float(request.form['y'])
        z = float(request.form['z'])
        price = request.form['price']

        # df.loc[df.index.size] = [carat, cut, color, clarity,
        #                         depth, x, y, z, price]
        # Data frame to CSV file
        # df.to_csv('./data/diamond.csv', index=False)
        return render_template('ok.html')
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    @app.route('/predict', methods=['POST'])
    def predict_item():
        global df
        print("Hello from predict_item on dataroutes.py")
        carat = request.form['carat']
        cut = request.form['cut']
        color = request.form['color']
        clarity = request.form['clarity']
        depth = float(request.form['depth'])
        table = float(request.form['table'])
        x = float(request.form['x'])
        y = float(request.form['y'])
        z = float(request.form['z'])

        # Open The model
        f = open('model_rf.pkl', 'rb')
        model_rf = pickle.load(f)
        f.close()

        # ls = [carat, table, depth, x, y, z]
        # index = 50000
        # carat = 0.23
        # cut = Ideal
        # depth = 61.5
        # table = 55.0
        # x = 3.95
        # y = 3.98
        # z = 2.43

        d_cut = {'Ideal': 1, 'Premium': 2, 'Very Good': 3,
                 'Good': 4, 'Fair': 5}
        d_color = {'G': 1, 'E': 2, 'F': 3, 'H': 4, 'D': 5,
                   'I': 6, 'J': 7}
        d_clarity = {'SI1': 1, 'VS2': 2, 'SI2': 3, 'VS1': 4, 'VVS2': 5,
                     'VVS1': 6, 'IF': 7, 'I1': 8}

        def cut_code(key_val):
            return d_cut[key_val]

        def color_code(key_val):
            return d_color[key_val]

        def clarity_code(key_val):
            return d_clarity[key_val]

        cut = cut_code(cut)
        color = color_code(color)
        clarity = clarity_code(clarity)
        rs = [carat, cut, color, clarity, depth, table, x, y, z]

        v = model_rf.predict([rs])

        return render_template('res.html', val=v)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    @app.route('/buildmodel')
    def build_a_model():
        print("Hello from build_a_model on dataroutes.py")
        handlers.buildmodel.build_it()
        print("End build The model")
        # flash('Process complete!')
        return render_template('buildmodel.html')

    @app.route('/fetch_data')
    def improve_model():
        print("Hello from improve_model on dataroutes.py")
        # flash('Process complete!')
        return render_template('admin.html')

    @app.route('/database/dp_db_install')
    def dp_install():
        init_df()
        database.dp_db_settings.dp_initial_globals()
        print("Hello from dp_install on dataroutes.py")
        # flash('Process complete!')
        database.dp_db_settings.dp_db_install.start()
        return ('', 204)
#   @app.route('/database/dp_db_creation')
#   def dp_db_creation():
#       print("Hello from connectivity_check on dataroutes.py")
#       # flash('Process complete!')
#       database.dp_db_creation.create_database(cursor)
#       return render_template('admin.html')

    @app.route('/database/dp_db_drop+install')
    def dp_install_drop():
        print("Hello from dp_install_drop on dataroutes.py")
        # flash('Process complete!')
        init_df()
        dp_db_install.start(drop=1)
        return('', 204)

    @app.route('/database/dp_db_insert')
    def dp_insert():
        print("Hello from dp_insert on dataroutes.py")
        database.dp_db_insert.dp_diamond()
        return('', 204)
