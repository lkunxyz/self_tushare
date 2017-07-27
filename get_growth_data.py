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
        profits = ts.get_growth_data(i, j+1);
        for index,row in profits.head(1).iterrows():
            for idx in range(len(row)):
                    if(isinstance(row[idx], float) and math.isnan(row[idx])):
                        row[idx] = 0;
            
            sql = "insert into t_growth_data(code, timestamp, mbrg, nprg, nav, targ, epsg, seg) values ('%s', '%s', %f, %f, %f, %f, %f, %f) on duplicate key update mbrg=%f, nprg=%f, nav=%f, targ=%f, epsg=%f, seg=%f" %(row.code, timestamp, row.mbrg, row.nprg, row.nav, row.targ, row.epsg, row.seg, row.mbrg, row.nprg, row.nav, row.targ, row.epsg, row.seg) 
            print sql
            cur.execute(sql)

cur.close()
conn.commit()
