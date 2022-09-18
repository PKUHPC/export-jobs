# -*- coding: UTF-8 -*-

from mysql import Mysql
from config import cluster_db_conf,mgt_db_conf,cluster_name
from util import parse_tres, parse_gres
import time,datetime

class Job:
    def __init__(self,info_list={},cluster=cluster_name):
        self.qos            = info_list['qos'] if 'qos' in info_list else '-'
        self.job_db_inx     = int(info_list['job_db_inx']) if 'job_db_inx' in info_list else 0
        self.id_job         = int(info_list['id_job']) if 'id_job' in info_list else 0
        self.account        = info_list['account'] if 'account' in info_list else '-'
        self.user           = info_list['user'] if 'user' in info_list else '-'
        self.partition      = info_list['partition'] if 'partition' in info_list else '-'
        self.nodelist       = info_list['nodelist'] if 'nodelist' in info_list else '-'
        self.job_name       = str(info_list['job_name']) if 'job_name' in info_list else '-'
        self.state          = info_list['state'] if 'state' in info_list else 'UNKNOW'
        self.time_submit    = int(info_list['time_submit']) if 'time_submit' in info_list else 0
        self.time_start     = int(info_list['time_start']) if 'time_start' in info_list else 0
        self.time_end       = int(info_list['time_end']) if 'time_end' in info_list else 0
        self.gpu            = int(info_list['gpu_alloc']) if 'gpu' in info_list else 0
        self.cpus_req       = int(info_list['cpus_req']) if 'cpus_req' in info_list else 0
        self.mem_req        = int(info_list['mem_req']) if 'mem_req' in info_list else 0
        self.nodes_req      = int(info_list['nodes_req']) if 'nodes_req' in info_list else 0
        self.cpus_alloc     = int(info_list['cpus_alloc']) if 'cpus_alloc' in info_list else 0
        self.mem_alloc      = int(info_list['mem_alloc']) if 'mem_alloc' in info_list else 0
        self.nodes_alloc    = int(info_list['nodes_alloc']) if 'nodes_alloc' in info_list else 0
        self.timelimit      = int(info_list['timelimit']) if 'timelimit' in info_list else 0
        self.time_used      = int(info_list['time_used']) if 'time_used' in info_list else 0
        self.time_wait      = int(info_list['time_wait']) if 'time_wait' in info_list else 0

        self.tres_alloc     = info_list['tres_alloc'] if 'tres_alloc' in info_list else ''
        self.tres_req       = info_list['tres_req'] if 'tres_req' in info_list else ''

        self.price          = int(info_list['price']) if 'price' in info_list else 0
        self.info           = info_list['info'] if 'info' in info_list else '-'

    def get_readable_job(self):
        readable_job = self.__dict__
        readable_job["time_used"]   = readable_job['time_end']-readable_job['time_start']
        readable_job["time_wait"]   = readable_job['time_start']-readable_job['time_submit']
        readable_job["cpus_req"],readable_job["mem_req"],readable_job["nodes_req"]         = parse_tres(readable_job['tres_req'])
        readable_job["cpus_alloc"],readable_job["mem_alloc"],readable_job["nodes_alloc"]   = parse_tres(readable_job['tres_alloc'])
        readable_job["time_submit"] = time.strftime("%Y%m%d-%H:%M:%S",time.localtime(readable_job["time_submit"]))
        readable_job["time_start"] = time.strftime("%Y%m%d-%H:%M:%S",time.localtime(readable_job["time_start"]))
        readable_job["time_end"] = time.strftime("%Y%m%d-%H:%M:%S",time.localtime(readable_job["time_end"]))
        return readable_job

    def get_end_date(self):
        return time.strftime("%Y%m%d",time.localtime(self.time_end))

class BIJob(Job):

    def __init__(self,info_list={},cluster=cluster_name):
        Job.__init__(self,info_list)
        self.time_submit    = self._get_timestamp(info_list['time_submit'] if 'time_submit' in info_list else 0)
        self.time_start     = self._get_timestamp(info_list['time_start'] if 'time_start' in info_list else 0)
        self.time_end       = self._get_timestamp(info_list['time_end'] if 'time_end' in info_list else 0)
        self.cluster=cluster

    def _get_timestamp(self,timestamp):
        if timestamp == 0:
            return datetime.datetime.now()
        else:
            return datetime.datetime.fromtimestamp(timestamp)

    @staticmethod
    def insert_sql_keys():
        return ['id_job','account','user','partition','nodelist','job_name',
            'cluster','time_submit','time_start','time_end','gpu','cpus_req',
            'mem_req','nodes_req','cpus_alloc','mem_alloc','nodes_alloc',
            'timelimit','time_used','time_wait','qos']

    def insert_sql_value(self):
        try:
            insert_sql = "{id_job},'{account}','{user}','{partition}','{nodelist}',\
                '{job_name}','{cluster}','{time_submit}','{time_start}','{time_end}',\
                {gpu},{cpus_req},{mem_req},{nodes_req},{cpus_alloc},{mem_alloc},\
                {nodes_alloc},{timelimit},{time_used},{time_wait},'{qos}'".format(
                    id_job=self.id_job,
                    account=self.account,
                    user=self.user,
                    partition=self.partition,
                    nodelist=self.nodelist,
                    #job_name=self.job_name.encode("UTF-8"),
                    job_name=self.job_name,
                    cluster=self.cluster,
                    time_submit=self.time_submit,
                    time_start=self.time_start,
                    time_end=self.time_end,
                    gpu=self.gpu,
                    qos=self.qos,
                    cpus_req=self.cpus_req,
                    mem_req=self.mem_req,
                    nodes_req=self.nodes_req,
                    cpus_alloc=self.cpus_alloc,
                    mem_alloc=self.mem_alloc,
                    nodes_alloc=self.nodes_alloc,
                    timelimit=self.timelimit,
                    time_used=self.time_used,
                    time_wait=self.time_wait)
        except:
            print(self.__dict__)
            print(type(self.qos))
            raise
        return insert_sql


class ClusterJobs:
    def __init__(self,cluster=cluster_name,job_list=[],job_cls=Job):
        self.cluster = cluster
        self.job_list = job_list
        self.db_conf = cluster_db_conf
        self._db = None
        # TODO Add try except
        self.job_cls = job_cls

    @property
    def db(self):
        if self._db == None:
            # TODO Add try except
            return Mysql(self.db_conf)
        else:
            return self._db

    def get_job_from_slurm(self,start=0,end=0):
        if start == end:
            return

        sql_str = "select\
            {job_table}.job_db_inx,\
            {job_table}.id_job,\
            {job_table}.account,\
            {assoc_table}.user,\
            {job_table}.partition,\
            {job_table}.time_submit,\
            {job_table}.time_start,\
            {job_table}.time_end,\
            {job_table}.nodelist,\
            {job_table}.job_name,\
            {job_table}.timelimit,\
            {qos_table}.name,\
            {job_table}.tres_alloc,\
            {job_table}.tres_req\
            from {qos_table},{job_table},{assoc_table} where\
            {job_table}.id_qos=qos_table.id and \
            {job_table}.id_assoc={assoc_table}.id_assoc and \
            {job_table}.time_start>0 and \
            {job_table}.time_end>{start} and \
            {job_table}.time_end<={end}".format(
                start=start,end=end,
                job_table = cluster_name + '_job_table',
                qos_table = "qos_table",
                assoc_table = cluster_name + '_assoc_table',
            )

        # TODO Add try except
        ret_list = self.db.execute(sql_str)
        job_list = []
        for ret in ret_list:
            job = ret
        #    job['gpu']         = parse_gres(job['gres_req'])
            job["time_used"]   = job['time_end']-job['time_start']
            job["time_wait"]   = job['time_start']-job['time_submit']
            job["cpus_req"],job["mem_req"],job["nodes_req"],job["gpu_req"]         = parse_tres(job['tres_req'])
            job["cpus_alloc"],job["mem_alloc"],job["nodes_alloc"],job["gpu_alloc"] = parse_tres(job['tres_alloc'])
            job['qos'] = job['name']
            job_list.append(self.job_cls(info_list=job,cluster=self.cluster))
        self.job_list=job_list

    # 按日期将作业分类，返回 {日期:[job,job]}
    def classify_jobs_by_day(self):
        ret = {}
        for job in self.job_list:
            job_end_date = job.get_end_date()
            if job_end_date in ret.keys():
                ret[job_end_date].append(job)
            else:
                ret[job_end_date] = [job]
        return ret
