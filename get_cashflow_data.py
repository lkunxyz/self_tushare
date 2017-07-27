# -*- coding:utf8 -*-

import MySQLdb;
import PySQLPool;
import tushare as ts;

import sys, math, json;
reload(sys);
sys.setdefaultencoding('utf-8') 

def get_conf(file):
    with open(file) as json_file:
        data = json.load(json_file)
        return data

def format_data(row):
    for idx in range(len(row)):
        if(isinstance(row[idx], float) and math.isnan(row[idx])):
            row[idx] = 0;
    return row


conf = get_conf('conf.ini')
conn = PySQLPool.getNewConnection(host=conf['host'], port=conf['port'], user=conf['user'], passwd=conf['passwd'], db=conf['db'], charset='utf8')
query = PySQLPool.getNewQuery(conn);

years = [2016]
for i in years:
    for j in range(4):
        timestamp = "%d0%d" %(i, j+1)
        profits = ts.get_cashflow_data(i, j+1);
        for index,row in profits.head(1).iterrows():
            row = format_data(row); 
            sql = "insert into t_cashflow_data(code, cf_sales, rateofreturn, cf_nm, cf_liabilities, cashflowratio, timestamp) values ('%s', %f, %f, %f, %f, %f, '%s') on duplicate key update cf_sales=%f, rateofreturn=%f, cf_nm=%f, cf_liabilities=%f, cashflowratio=%f" %(row.code, row.cf_sales, row.rateofreturn, row.cf_nm, row.cf_liabilities, row.cashflowratio, timestamp, row.cf_sales, row.rateofreturn, row.cf_nm, row.cf_liabilities, row.cashflowratio) 
            print sql
            query.Query(sql)
