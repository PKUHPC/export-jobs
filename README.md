# 配置源作业信息数据库

此项目负责定时地将slurm集群中的已完成的作业信息移动到另一个数据库中，主要用于SCOW的计费收费。

https://pkuhpc.github.io/SCOW/docs/deploy/SCOW/mis

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

1. 部署源作业数据库

```bash
# (1) 创建mysql数据库
# SCOW部署节点已安装docker,可在该节点上用docker起一个mysql作为源作业数据库
# 源作业数据库需要将3306端口暴露给export-jobs使用，host_port为宿主机端口，确保该端口未被其他服务占用。可通过宿主机ip:host_port访问到源作业数据库，password为数据库的root密码。
docker run --restart=always --name sourcedb -p {host_port}:3306 -e MYSQL_ROOT_PASSWORD='{password}' -d mysql:8

# (2) 设置允许远程访问
#  进入容器
docker exec -it sourcedb /bin/bash
# 登录
mysql -uroot -p

# 允许远程访问
grant all privileges on *.* to 'root'@'%' ;
flush privileges;

# (3) 创建数据库
CREATE DATABASE hpc;
use hpc;

# (4) 数据库初始化,创建job_table表，建表语句为export-jobs/job_table.sql文件
CREATE TABLE `job_table` (
  `bi_job_index` int(10) NOT NULL AUTO_INCREMENT,
  `id_job` int(10) unsigned NOT NULL,
  `account` tinytext NOT NULL COMMENT '账户',
  `user` varchar(127) NOT NULL COMMENT '用户名',
  `partition` tinytext NOT NULL COMMENT '分区',
  `nodelist` text NOT NULL COMMENT '使用节点列表',
  `job_name` tinytext NOT NULL COMMENT '作业名',
  `cluster` varchar(50) NOT NULL COMMENT '集群名',
  `time_submit` datetime NOT NULL COMMENT '提交时间',
  `time_start` datetime NOT NULL COMMENT '开始时间',
  `time_end` datetime NOT NULL COMMENT '结束时间',
  `gpu` int(10) NOT NULL DEFAULT '0' COMMENT '使用GPU数，来自gres_req字段',
  `cpus_req` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '申请CPU数tres_req',
  `mem_req` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '申请的内存，单位MB，来自tres_req',
  `nodes_req` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '申请节点数tres_req',
  `cpus_alloc` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '分配CPU数tres_alloc',
  `mem_alloc` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '分配的内存，单位MB，来自tres_alloc',
  `nodes_alloc` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '分配节点数tres_alloc',
  `timelimit` int(10) unsigned NOT NULL COMMENT '作业时间限制',
  `time_used` bigint(20) unsigned NOT NULL COMMENT '作业执行时间',
  `time_wait` bigint(20) unsigned NOT NULL COMMENT '作业等待时间',
  `qos` varchar(255) NOT NULL,
  `record_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录时间',
  PRIMARY KEY (`bi_job_index`),
  KEY `time_submit` (`time_submit`) USING BTREE,
  KEY `time_start` (`time_start`) USING BTREE,
  KEY `time_end` (`time_end`) USING BTREE,
  KEY `time_used` (`time_used`) USING BTREE,
  KEY `time_wait` (`time_wait`) USING BTREE,
  KEY `user` (`user`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=25559 DEFAULT CHARSET=utf8;
```

2. 修改配置文件

```shell
# cat  config.py

# slurm集群名称
cluster_name = 'hpc01'

# slurm数据库相关配置
cluster_db_conf = {
    'host':'localhost',			# 修改为部署slurm数据库的节点IP
    'port':3306,
    'user':'username',
    'passwd':'passwd',
    'db':'slurm_acct_db',
    'gres_id' : 1001
}

# 源数据库相关配置
mgt_db_conf = {
    'host':'remote_host',		# 部署源作业数据库节点的IP
    'port':3306,				# 修改为docker -p 的{host_port}
    'user':'username',
    'passwd':'password',
    'db':'hpc'
}
```



3. 安装Python依赖。以下`/path/to/export_jobs`替换为clone本仓库后的地址。

```bash
pip3 install -f /path/to/export_jobs/requirements.txt
```

4. 尝试获取信息

```bash
python3 /path/to/export_jobs/main.py
```

5. 设置每10分钟执行的定时任务。频率可自己定义。

```bash
echo "*/10 * * * * root python3 /path/to/export_jobs/main.py >> /path/to/export_jobs/job_export.log 2>&1" >> /etc/crontab
```