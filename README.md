# 配置源作业信息数据库

导出集群slurm数据库中已完成的作业信息到源作业信息数据库job_table表，用于SCOW的计费收费。

https://pkuhpc.github.io/SCOW/docs/mis/deployment/job_table

## 配置说明

配置内容在config.py中：

| 字段名                  | 说明                     |
| ----------------------- | ------------------------ |
| cluster_name            | slurm中集群的名称        |
| cluster_db_conf         | 集群slurm数据库信息      |
| cluster_db_conf.host    | slurm数据库ip            |
| cluster_db_conf.port    | slurm数据库端口          |
| cluster_db_conf.user    | slurm数据库用户名        |
| cluster_db_conf.passwd  | slurm数据库密码          |
| cluster_db_conf.db      | slurm数据库名            |
| cluster_db_conf.gres_id | slurm中gpu资源的id       |
| mgt_db_conf             | 存放作业的远端数据库配置 |
| mgt_db_conf.host        | 源作业信息数据库ip       |
| mgt_db_conf.port        | 源作业信息数据库端口     |
| mgt_db_conf.user        | 源作业信息数据库用户名   |
| mgt_db_conf.passwd      | 源作业信息数据库密码     |
| mgt_db_conf.db          | 源作业信息数据库数据库名 |

## 运行说明

需要Python 3环境。

1. 安装mariadb

```bash
# 以CentOS 7举例
yum install mariadb mariadb-server
systemctl enable --now mariadb
# 配置密码
mysql_secure_installation
```

2. 安装Python依赖。以下`/path/to/export_jobs`替换为clone本仓库后的地址。

```bash
pip3 install -f /path/to/export_jobs/requirements.txt
```

3. 尝试获取信息

```bash
python3 /path/to/export_jobs/main.py
```

3. 设置每10分钟执行的定时任务。频率可自己定义。

```bash
echo "*/10 * * * * root python3 /path/to/export_jobs/main.py >> /path/to/export_jobs/job_export.log 2>&1" >> /etc/crontab
```