DROP TABLE IF EXISTS `job_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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