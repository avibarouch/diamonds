# import database.dp_db_insert
from flask import *  # request, render_template
import json
import pandas as pd
import pickle
import handlers.dp_buildmodel
import database.dp_db_install
import dp_forms
import database.dp_db_insert
import handlers.dp_predict
import dp_db_insert

flag = 0
df = None


def init_df():
    global df, flag

    if flag == 0:
        flag = 1
        df = pd.read_csv('./data/diamond.csv').head(20)


def configure(app):

    @app.route('/details/<int:id>')
    def getdetails(id):
        global df
        print("Hello from predict_item on dataroutes.py")
        return render_template('details.html', item=df.iloc[id])

    @app.route('/res')
    def dp_res():
        return render_template("res.html")

    @app.route('/predict', methods=['GET', 'POST'])
    def predict():
        form = dp_forms.Predict_form()
        if form.validate_on_submit():
            # ToDo: flash this messese in green color
            flash('Got your data. '
                  'carat={}, cut={} and so on ... Thank you!'
                  .format(form.carat.data, form.cut.data))
            diamond = {}
            diamond['carat'] = float(form.carat.data)
            diamond['cut'] = form.cut.data
            diamond['color'] = form.color.data
            diamond['clarity'] = form.clarity.data
            diamond['depth'] = float(form.depth.data)
            diamond['table'] = float(form.table1.data)
            diamond['x'] = float(form.x.data)
            diamond['y'] = float(form.y.data)
            diamond['z'] = float(form.z.data)
            price = handlers.dp_predict.diamond_price(diamond)
            return render_template('res.html', price=price)
        return render_template('predict.html', form=form)

    @app.route('/addnew', methods=['GET', 'POST'])
    def addnew():
        form = dp_forms.Addnwew_form()
        if form.validate_on_submit():
            # ToDo: flash this messese in green color
            flash('Got your data. '
                  'carat={}, cut={}, price={} ... Thank you!'
                  .format(form.carat.data, form.cut.data, form.price.data))
            diamond = {}
            diamond[0] = form.carat.data
            diamond[1] = form.cut.data
            diamond[2] = form.color.data
            diamond[3] = form.clarity.data
            diamond[4] = form.depth.data
            diamond[5] = form.table1.data
            diamond[6] = form.price.data
            diamond[7] = form.x.data
            diamond[8] = form.y.data
            diamond[9] = form.z.data
            database.dp_db_insert.me(diamond)
            return redirect('/addnew')
        return render_template('addnew.html', form=form)

    @app.route('/database/dp_db_install')
    def dp_install():
        flash("The insert process can take some time.")
        render_template(admin.html)
        database.dp_db_install.start()
        flash("Thank you for you'r paition")
        return render_template("admin.html")

    @app.route('/database/dp_db_drop')
    def dp_db_drop():
        flash("Begin of Droping process")
        database.dp_db_install.start(drop=1)
        flash('End of Droping process')
        return render_template("admin.html")

    @app.route('/')
    def hello_world():
        global df
        init_df()
        return render_template('main.html', data=df)

    @app.route('/admin')
    def admin():
        return render_template('admin.html')

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
        return render_template('ok.html')

    @app.route('/buildmodel')
    def build_a_model():
        flash("Start Build a model")
        handlers.dp_buildmodel.build_it()
        flash("End build The model")
        return render_template('buildmodel.html')

    @app.route('/insert_data')
    def improve_model():
        flash("Begin of insert new data")
        database.dp_db_install.start()
        flash('End of insert new data')
        return render_template('admin.html')

    @app.route('/database/dp_db_insert')
    def dp_db_insert():
        database.dp_db_insert.dp_diamond(drop=0)
        return("/admin", 204)
