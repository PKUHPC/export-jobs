# -*- coding: UTF-8 -*-
import datetime,time
from TransformJobToBI import TransformJobToBI

if __name__ == "__main__":
    # 每10分钟统计一次作业信息，生成计费用的报表并写到BI数据库里面
    to_date_minite = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    to_date = to_date_minite[:-1]+"000"
    from_date_minite = (datetime.datetime.now() + datetime.timedelta(minutes=-10)).strftime("%Y%m%d-%H%M")
    #from_date_minite = (datetime.datetime.now() + datetime.timedelta(days=-240)).strftime("%Y%m%d-%H%M")
    from_date = from_date_minite[:-1]+"000"
    from_timestamp = time.mktime(time.strptime(from_date,"%Y%m%d-%H%M%S"))
    to_timestamp = time.mktime(time.strptime(to_date,"%Y%m%d-%H%M%S"))

    transform_process = TransformJobToBI(from_time=from_timestamp,to_time=to_timestamp)
    num = transform_process.execute()
    print(from_date,to_date,num)
