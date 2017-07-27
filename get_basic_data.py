# -*- coding:utf8 -*-

import MySQLdb;
import PySQLPool;
import tushare as ts;

import sys, math;
reload(sys);
sys.setdefaultencoding('utf-8') 

conn = PySQLPool.getNewConnection(host='10.211.55.5', port=3306, user='analysis', passwd='analysis@sec', db='db_sina_data', charset='utf8')
query = PySQLPool.getNewQuery(conn);
basics = ts.get_stock_basics();
for index,row in basics.iterrows():
    params = "'" + str(index) + "'";
    for i in range(len(row)):
        if(isinstance(row[i], float) and math.isnan(row[i])):
            row[i] = 0
        
        params += ','
        if(isinstance(row[i],str)):
            params += "'"
        params += str(row[i])
        if(isinstance(row[i],str)):
            params += "'"

    sql = 'insert into t_stock_code(code, name,industry, area, pe, outstanding, totals, totalAssets, liquidAssets, fixedAssets, reserved, reservedPerShare, esp, bvps, pb, timeToMarket, undp, perundp, rev, profit, gpr, npr, holders) values (' + params + ') on duplicate key update code=values(code)'
    query.Query(sql)
