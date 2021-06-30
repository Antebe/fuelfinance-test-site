# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 13:34:18 2020

@author: hp
"""
from config import USER, PASSWORD
import pymysql
import aws_credentials as rds
conn = pymysql.connect(
        host= "database-main.capvj7ilkznh.us-east-2.rds.amazonaws.com", #endpoint link
        port = 3306, # 3306
        user = "admin",
        password = "120807zzZ!",
        db = "transactions", #test
        )
#
#
# cursor=conn.cursor()
# create_table="""
# create table NewTable (date varchar(2000),summ varchar(2000),account varchar(200),purpose varchar(2000), CFACC varchar(200), PLAcc varchar (200))
#
# """
# cursor.execute(create_table)
import string
def get_table_by_id(id):
    cur = conn.cursor()
    cur.execute('SELECT database_id FROM accounts WHERE id = % s', (id))
    details = cur.fetchall()
    return str(details[0]).translate(str.maketrans('', '', string.punctuation))

def check_account(email, id):
    cur=conn.cursor()
    cur.execute('SELECT * FROM accounts WHERE email = % s AND id = % s', (email, id))
    account = cur.fetchone()
    return account

def setup_updating():
    cursor = conn.cursor(pymysql.cursors.DictCursor)

def insert_details(id, date, summ, account, purpose, CFAcc, PLAcc, table):
    cur=conn.cursor()
    cur.execute("INSERT INTO " + table + " (id, date, summ, account, purpose, CFAcc, PLAcc) VALUES (%s,%s,%s,%s,%s,%s,%s)", (id, date, summ, account, purpose, CFAcc, PLAcc))
    conn.commit()

def get_details(table):
    cur=conn.cursor()
    cur.execute("SELECT *  FROM " + table)
    details = cur.fetchall()
    return details

def last_five(table):
    cur=conn.cursor()
    cur.execute("SELECT * FROM " + table + " ORDER BY id DESC LIMIT 5")
    results = cur.fetchall()
    return results

def all_items(table):
    cur=conn.cursor()
    cur.execute("SELECT * FROM " + table +" ORDER BY id DESC")
    results = cur.fetchall()
    return results


def update_data(field, value, editid, table):
    # select what to edit
    if field == 'date':
        sql = "UPDATE " +table+ " SET date=%s WHERE id=%s"
    if field == 'summ':
        sql = "UPDATE " + table + " SET summ=%s WHERE id=%s"
    if field == 'account':
        sql = "UPDATE "+table+" SET account=%s WHERE id=%s"
    if field == 'purpose':
        sql = "UPDATE "+table+" SET purpose=%s WHERE id=%s"
    if field == 'CFAcc':
        sql = "UPDATE "+table+" SET CFACC=%s WHERE id=%s"
    if field == 'PLAcc':
        sql = "UPDATE "+table+" SET PLAcc=%s WHERE id=%s"

    data = (value, editid)
    cursor = conn.cursor()
    cursor.execute(sql, data)
    conn.commit()
    success = 1


def itemslists(table):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * from "+table+" order by id DESC")
    itemslists = cursor.fetchall()
    return itemslists