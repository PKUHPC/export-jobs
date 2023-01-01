# -*- coding: UTF-8 -*-
from Job import BIJob,ClusterJobs

import time

from config import *
from mysql import Mysql

class TransformJobToBI():
    def __init__(self,from_time,to_time=None):
        # from_time 统计开始时间戳，
        # to_time 统计结束时间戳，默认为当前时间戳
        if to_time is None:
            to_time = int(time.time())
        self.to_time = to_time
        self.from_time = from_time
        self._bi_db = None

    @property
    def bi_db(self):
        if self._bi_db == None:
            self._bi_db = Mysql(mgt_db_conf)
        return self._bi_db

    def execute(self,cluster=cluster_name):
        cluster_jobs = ClusterJobs(cluster=cluster,job_cls=BIJob)
        cluster_jobs.get_job_from_slurm(self.from_time,self.to_time)
        list_length=len(cluster_jobs.job_list)
        #print(list_length)
        # return
        insert_sql = "insert into job_table (`{keys}`) values ".format(
            keys= "`,`".join(BIJob.insert_sql_keys())
        )
        index=0
        page=0
        interval=5000
        for job in cluster_jobs.job_list:
            insert_sql = insert_sql + "({}),".format(job.insert_sql_value())
            index += 1
            if index == interval:
                #print(page,list_length/interval,time.strftime("%Y%m%d-%H:%M:%S"))
                #print(insert_sql[:-1])
                self.bi_db.execute(insert_sql[:-1])
                self.bi_db.commit()
                index=0
                page+=1
                insert_sql = "insert into job_table ({keys}) value ".format(
                    keys= ",".join(BIJob.insert_sql_keys())
                )
        if list_length>0:
            self.bi_db.execute(insert_sql[:-1])
            self.bi_db.commit()
        return list_length
