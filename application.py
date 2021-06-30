# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 12:02:51 2020

@author: hp
"""
import test

import gspread
import datetime
from flask import Flask, render_template, request, flash, redirect,url_for, jsonify, session

from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from flask import Response,send_file

application = Flask(__name__)

application.secret_key = 'secretkey'

import rds_db as db

#connecting to google tables

@application.route('/')
@application.route('/login', methods =['GET', 'POST'])
def index():

    msg = ''
    global session
    #основні дані про юзера
    session = {
        "loggedin": False,
        "id":"",
        "email":"",
        "table":"",
    }
    if request.method == 'POST' and 'email' in request.form and 'id' in request.form:
        global email
        global id_user
        email = request.form['email']
        id_user = request.form['id']
        account = db.check_account(email, id_user)
        if account:
            session['loggedin'] = True
            session['id'] = id_user
            session['email'] = email
            session['table'] = db.get_table_by_id(id_user)
            print(session)

            # getting last 5 rows
            details = db.last_five(session['table'])
            data = []
            for detail in details:
                data.append(detail)

            #set up google sheets for this account
            global table_id
            global worksheet
            table_id = str(id_user)

            gc = gspread.service_account(filename="credit.json")
            sh = gc.open_by_key(table_id)
            worksheet = sh.sheet1

            #справочникu
            global handbook
            global handbook_acc

            handbook = [item for item in worksheet.col_values(8) if item]
            handbook_acc = [item for item in worksheet.col_values(9) if item]
            handbook.pop(0)#всі статті у колонці "H" таблички
            handbook_acc.pop(0)
            print(handbook_acc)

            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg, data = data, handbook = handbook, handbook_acc = handbook_acc)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@application.route('/home',methods = ['post'])
def home():
    handbook = [item for item in worksheet.col_values(8) if item]
    handbook_acc = [item for item in worksheet.col_values(9) if item]
    print(handbook_acc)
    handbook.pop(0)  # всі статті у колонці "H" таблички
    handbook_acc.pop(0)

    # getting last 5 rows
    details = db.last_five(session['table'])
    data = []
    for detail in details:
        data.append(detail)
    return render_template("index.html", data=data, handbook = handbook, handbook_acc = handbook_acc)

@application.route('/insert',methods = ['post'])
def insert():
    # getting last 5 rows
    details = db.last_five(session['table'])
    data = []
    for detail in details:
        data.append(detail)

    if request.method == 'POST':
        id = test.create_id()
        date = request.form['date']
        summ = request.form['summ']
        account = request.form['account']
        purpose = request.form['purpose']
        CFAcc = request.form['CFAcc']
        PLAcc = request.form['PLAcc']
        db.insert_details(id, date, summ, account, purpose, CFAcc, PLAcc, session['table'])


        #submitting to google sheets last entry from db
        last_details = db.get_details(session['table'])
        details_last = list(last_details[-1])
        print(details_last)

        worksheet.append_row(details_last)

        details = db.last_five(session['table'])
        data = []
        for detail in details:
            data.append(detail)

        return render_template('index.html',data=data)

@application.route('/full_table')
def full_table():
    items = db.itemslists(session['table'])
    return render_template('full_table.html', userslist = items)

@application.route("/full_table_updated", methods=["POST", "GET"])
def update():
    try:
        db.setup_updating()
        if request.method == 'POST':
            field = request.form['field']
            print(field)
            value = request.form['value']
            print(value)
            editid = request.form['id']
            print(editid)
            db.update_data(field, value, editid, session['table'])

            #update google sheets by id
            cell_target = worksheet.find(editid)
            cell_field = worksheet.find(field)
            worksheet.update_cell(cell_target.row, cell_field.col, value)
            print(cell_target.row, cell_field.col, value)


        return jsonify(1)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    application.run(debug=True)