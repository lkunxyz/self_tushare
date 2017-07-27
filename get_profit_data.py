# -*- coding:utf8 -*-

import MySQLdb;
import tushare as ts;

import sys, math;
reload(sys);
sys.setdefaultencoding('utf-8') 

conn = MySQLdb.connect(host='10.211.55.5', port=3306, user='analysis', passwd='analysis@sec', db='db_sina_data', charset='utf8')
cur = conn.cursor()
for i in [2016, 2017]:
    for j in range(4):
        timestamp = "%d0%d" %(i, j+1)
        profits = ts.get_profit_data(i, j+1);
        for index,row in profits.head(3).iterrows():
            for idx in range(len(row)):
                    if(isinstance(row[idx], float) and math.isnan(row[idx])):
                        row[idx] = 0;
            
            sql = "insert into t_profit_data(code, timestamp, roe, net_profit_ratio, gross_profit_rate, net_profits, eps, business_income, bips) values ('%s', '%s', %f, %f, %f, %f, %f, %f, %f) on duplicate key update roe=%f, net_profit_ratio=%f, gross_profit_rate=%f, net_profits=%f, eps=%f, business_income=%f,bips=%f" %(row.code, timestamp, row.roe, row.net_profit_ratio, row.gross_profit_rate, row.net_profits, row.eps, row.business_income, row.bips, row.roe, row.net_profit_ratio, row.gross_profit_rate, row.net_profits, row.eps, row.business_income, row.bips) 
            #print sql
            cur.execute(sql)

cur.close()
conn.commit()
