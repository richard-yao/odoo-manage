# -*- coding: utf-8 -*-

import xmlrpclib
import mysql.connector
from createModel import CustomModel

url = 'http://10.12.22.201:8069'
db = 'account_test'
username = 'richardyao@tvunetworks.com'
password = 'richardyao'
x_model = 'x_salesforce_account'
db_config = {
    'user': 'root',
    'password': 'admin',
    'host': 'localhost',
    'database': 'tp',
}

def checkConnect():
    try:
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
        print common.version()
        return common
    except Exception as e:
        print e
        return

def authenticate(common):
    try:
        uid = common.authenticate(db, username, password, {})
        print "authenticate uid is {}".format(uid)
        return uid
    except Exception as e:
        print "Error: %s" %e

def readData(model, uid):
    filter = [['id', '>', 0]]
    ids = model.execute_kw(db, uid, password, 'account.account', 'search', [filter])
    print "ids value is %s " %[ids]

def fieldsGet(model, uid):
    key = 'fields_get'
    filter = {'attributes': ['string', 'help', 'type']}
    result = model.execute_kw(db, uid, password, 'res.partner', key, [], filter)
    print "query res.partner fields value %s" %result.get('signup_valid', 'Not Found')

def createRecord(model, uid):
    fields = ['x_account_id', 'x_account_name', 'x_account_type', 'x_account_region', 'x_account_parent_id']
    key = 'create'
    record = {'x_account_id': '0010G00001tOjiiQAC', 'x_account_name': 'Soft Skills', 'x_account_type': 'Analyst/Consultant;Systems Integrator', 'x_account_region': 'Asia Pacific - Non China', 'x_account_parent_id': ''}
    records = [record]
    id = model.execute_kw(db, uid, password, x_model, key, records)
    print "insert record successfully with %s" %id
    result = model.execute_kw(db, uid, password, x_model, 'search_read', [[['id', '>', 0]]], {'fields': fields, 'limit': 5})
    print "query record successfully with result: %s" %result

def insertDbRecordsToOdoo(model, uid):
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor(buffered=True)
    query = 'select account_id, name, type, sales_region, parent_id from sf_user limit 1'
    cursor.execute(query)
    key = 'create'
    number = 0
    for (account_id, name, type, sales_region, parent_id) in cursor:
        number += 1
        if type == None:
            type = ''
        if sales_region == None:
            sales_region = ''
        if parent_id == None:
            parent_id = ''
        record = {'x_account_id': account_id, 'x_account_name': name, 'x_account_type': type, 'x_account_region': sales_region, 'x_account_parent_id': parent_id}
        model.execute_kw(db, uid, password, x_model, key, [record])
    print "insert record successfully, total number is %s" %number

def main():
    common = checkConnect()
    uid = authenticate(common)
    model = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    customModel = CustomModel(model, uid, db, password)
    record_id = customModel.createModelIntoIrModel('x_custom_test', 'Test Table')
    fields = [{'model_id': record_id, 'name': 'x_custom_name', 'ttype': 'char', 'state': 'manual', 'required': True,}]
    customModel.createModelFields(fields)
    #print "model is %s, db is %s, uid is %s, password is %s" %(model, db, uid, password)
    #readData(model, uid)
    #fieldsGet(model, uid)
    #createRecord(model, uid)
    '''
    if 2 > 2:
        print "Success"
    elif 2 > 1:
        print "你好，中文"
    else: 
        print "11111"
    '''
    #insertDbRecordsToOdoo(model, uid)
main()