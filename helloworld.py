from flask import Flask, render_template,session,redirect,url_for,flash,request
# from flask.ext.bootstrap import Bootstrap
from flask_wtf import Form
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import create_engine,column
from sqlalchemy.orm import sessionmaker
from flask_restful import Resource, Api
import json
import psycopg2
import datetime
app = Flask(__name__)
bootstrap = Bootstrap(app)
CSRFProtect(app)
app.config["SECRET_KEY"] = 'hard to guess string'
# app.config["SQLALCHEMY_DATABASE_URI"]='postgressql://postgres:@localhost:5432/product'
# db = sqlalchemy(app)
conn = psycopg2.connect(
    host = '127.0.0.1',
    user = 'postgres',
    database = 'product',
    password = '',
    port = '5432'
)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

class NameForm(Form):
    name = StringField('What is your name?',validators=[DataRequired()])
    submit = SubmitField('Submit')

class SearchForm(Form):
    keyword = StringField("search by name or type",validators=[DataRequired()])
    submit = SubmitField('search')

class createForm(Form):
    name = StringField("NAME:",validators=[DataRequired()])
    type = StringField("TYPE:",validators=[DataRequired()])
    value = IntegerField("VALUE:",validators=[DataRequired()])
    # createdDate = DateField("CREATED DATE",validators=[DataRequired()])
    # changedDate = DateField("CHANGED DATE",validators=[DataRequired()])
    submit = SubmitField("save")

@app.route('/',methods=['GET','POST'])
def index():
    cur = conn.cursor()
    sql = "select * from product"
    cur.execute(sql)
    content = cur.fetchall()

    print(datetime.datetime.now().strftime('%Y-%m-%d'))
    keyword = None
    form1 = SearchForm()
    if form1.validate_on_submit():
        key = form1.keyword.data
        sql = "select * from product where product_name ='%s'"%key
        cur.execute(sql)
        content= cur.fetchall()
        if(content):
            flash("Have found result.")
            cotent = content
        else:
            sql = "select * from product where product_type ='%s'" % key
            cur.execute(sql)
            content = cur.fetchall()
            if(content):
                content = content
                flash("Have found result.")
            else:
                flash("There is no result, you can search by name or type.")


    return render_template('index.html',form1 = form1, content = content)

@app.route("/create", methods = ['GET','POST'])
def create():
    cur = conn.cursor()
    form = createForm()

    if form.validate_on_submit():
        name = form.name.data
        type = form.type.data
        value = form.value.data
        # create = form.createdDate.data
        # change = form.changedDate.data
        sql = "select * from product where product_name = '%s'"%name
        cur.execute(sql)
        content = cur.fetchall()
        if (content):
            flash("What you create already exists.")
        else:
            sql = "insert into product values(" + "'" + name + "'," + "'" + type + "'," + "'" + str(value) + "',current_date,current_date)"
            cur.execute(sql)
            conn.commit()
            flash("Success!")
    else:
        flash("Please check whether the form of data is right. E.g: VALUE should be number.")
    return render_template('create.html',form = form)

@app.route('/detail/<name>',methods = ['GET','POST'])
def detail(name):
    cur = conn.cursor()
    if request.method =='POST':
        result = request.form.to_dict()
        if(is_number(result['value'])):
            sql1 = "update product set product_name ='%s',product_type='%s',product_value='%s',changed_date=current_date where product_name = '%s'"%(result['name'],result['type'],result['value'],name)
            cur.execute(sql1)
            conn.commit()
            return redirect(url_for('detail',name = result['name']))
        else:
            flash("VALUE should be number")
            sql = "select * from product where product_name = " + "'" + name + "'"
            cur.execute(sql)
            content = (cur.fetchall())[0]
    else:
        sql = "select * from product where product_name = " + "'" + name + "'"
        cur.execute(sql)
        content = (cur.fetchall())[0]
    return render_template('detail.html',name = name ,content = content)

if __name__ == '__main__':
    app.run(debug=True)
