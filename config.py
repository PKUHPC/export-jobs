cluster_name="hpc01"

cluster_db_conf = {
    'host':'localhost',
    'port':3306,
    'user':'username',
    'passwd':'passwd',
    'db':'slurm_acct_db',
    'job_table':'cluster_job_table',
    'qos_table':'qos_table',
    'assoc_table':'cluster_assoc_table',
    'gres_id' : 1001
}

mgt_db_conf = {
    'host':'remote_host',
    'port':3306,
    'user':'username',
    'passwd':'password',
    'db':'hpc'
}
