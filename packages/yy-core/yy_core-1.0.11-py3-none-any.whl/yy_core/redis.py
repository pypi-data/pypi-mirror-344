# -*- coding: utf-8 -*-
"""
:Author: yy
:Date: 2020-04-16 14:38:22
@LastEditTime: 2025-04-28 16:17:59
@LastEditors: yy
:Description: redis helper
"""

from yy_core import *
import redis
from redis import RedisError
from redis.cluster import ClusterNode, RedisCluster

class RedisHelper:

    @classmethod
    def redis_init(self, host="", port=0, db=0, password=None, username=None, config_dict=None, decode_responses=False, ssl=False, ssl_cert_reqs=None, ssl_ca_certs=None):
        """
        :Description: 从redis连接池中创建对象
        :param host:主机地址
        :param port:端口
        :param db:redis_db
        :param password:授权密码
        :param username:授权用户名 支持>redis6.0
        :param ssl:是否启用ssl
        :param ssl_cert_reqs:启用安全级别
        :param ssl_ca_certs:启用PEM证书
        :return: redis客户端对象
        :last_editors: yy
        """
        if config_dict:
            if "host" in config_dict:
                host = config_dict["host"]
            if "port" in config_dict:
                port = config_dict["port"]
            if "db" in config_dict:
                db = config_dict["db"]
            else:
                db = 0
            if "username" in config_dict:
                username = config_dict["username"]
            if "password" in config_dict:
                password = config_dict["password"]
            if "ssl" in config_dict and config_dict["ssl"] == True:
                ssl = True
            if "ssl_cert_reqs" in config_dict and config_dict["ssl_cert_reqs"] == True:
                ssl_cert_reqs = True
            if "ssl_ca_certs" in config_dict and ssl_cert_reqs == True:
                ssl_ca_certs = ssl_ca_certs

        if not host or not port or host == "" or int(db) < 0 or int(port) <= 0:
            raise RedisError("Config Value Eroor")

        if ssl == True:
            pool = redis.ConnectionPool(host=host,
                                        port=port,
                                        db=db,
                                        username=username,
                                        password=password,
                                        decode_responses=decode_responses,
                                        connection_class=redis.connection.SSLConnection,
                                        ssl_cert_reqs=ssl_cert_reqs,
                                        ssl_ca_certs=ssl_ca_certs)
        else:
            pool = redis.ConnectionPool(host=host,
                                        port=port,
                                        db=db,
                                        username=username,
                                        password=password, decode_responses=decode_responses)

        redis_client = redis.Redis(connection_pool=pool)
        return redis_client

    @classmethod
    def redis_cluster_init(cls, config_dict):
        """
        :description: 
        :param config_dict: redis集群配置
        :return redis client
        :demo: 
            config:
                "redis": {
                    "cluster_nodes":[
                        {"host":"10.0.0.1","port":6379},
                        {"host":"10.0.0.2","port":6379}
                    ],
                    "password": "xxxxxxxx"
                }

                redis_client = RedisHelper.redis_cluster_init(config_dict=config.get_value("redis"))
                redis_client.get("test")

        :last_editors: yy
        """
        if not config_dict:
            raise RedisError("Config Value Eroor")

        username = None
        password = None

        cluster_nodes=[]
        if "cluster_nodes" in config_dict:
            for node in config_dict["cluster_nodes"]:
                if "host" not in node or "port" not in node:
                    raise RedisError("Config Value Eroor")
            cluster_nodes.append(ClusterNode(node["host"], node["port"]))

        if "username" in config_dict:
            username = config_dict["username"]

        if "password" in config_dict:
            password = config_dict["password"]

        if not cluster_nodes or len(cluster_nodes) == 0:
            raise RedisError("Config Value Eroor")

        # 创建RedisCluster实例
        return RedisCluster(startup_nodes=cluster_nodes, decode_responses=True,username=username, password=password)

        redis_clients = {}

    @classmethod
    def init(self, config_dict=None, decode_responses=True, go_heavy_connection=False):
        """
        :description: redis初始化
        :param config_dict：连接串配置
        :param decode_responses：是否解码输出
        :param go_heavy_connection：是否启用连接池对象去重,共用连接池对象
        :return: redis_client
        :last_editors: yy
        """
        if not config_dict:
            config_dict = config.get_value("redis")
        config_go_heavy_connection = share_config.get_value("go_heavy_connection", None)
        if config_go_heavy_connection != None:
            go_heavy_connection = config_go_heavy_connection
        if go_heavy_connection == False:
            redis_client = self.redis_init(config_dict=config_dict, decode_responses=decode_responses)
            return redis_client
        else:
            key = CryptoHelper.md5_encrypt(str(config_dict))
            if key in self.redis_clients.keys():
                return self.redis_clients[key]
            redis_client = self.redis_init(config_dict=config_dict, decode_responses=decode_responses)
            if redis_client:
                self.redis_clients[key] = redis_client
            return redis_client

    @classmethod
    def acquire_lock(self, lock_name, acquire_time=10, time_out=5, sleep_time=0.1, config_dict=None):
        """
        :description: 创建分布式锁 基于setnx命令的特性，我们就可以实现一个最简单的分布式锁了。我们通过向Redis发送 setnx 命令，然后判断Redis返回的结果是否为1，结果是1就表示setnx成功了，那本次就获得锁了，可以继续执行业务逻辑；如果结果是0，则表示setnx失败了，那本次就没有获取到锁，可以通过循环的方式一直尝试获取锁，直至其他客户端释放了锁（delete掉key）后，就可以正常执行setnx命令获取到锁
        :param lock_name：锁定名称
        :param acquire_time: 客户端等待获取锁的时间,单位秒,正常配置acquire_time<time_out
        :param time_out: 锁的超时时间,单位秒
        :param sleep_time: 轮询休眠时间,单位秒(需根据系统性能进行调整，值越小系统压力越大对系统的性能要求越高)
        :param config_dict：连接串配置
        :return 返回元组，分布式锁是否获得（True获得False未获得）和解锁钥匙（释放锁时需传入才能解锁成功）
        :last_editors: yy
        """
        identifier = str(uuid.uuid4())
        if share_config.get_value("is_pressure_test", False):  #是否进行压力测试
            return True, identifier
        end = time.time() + acquire_time
        lock = "lock:" + lock_name
        redis_init = self.init(config_dict=config_dict)
        while time.time() < end:
            if redis_init.setnx(lock, identifier):
                # 给锁设置超时时间, 防止进程崩溃导致其他进程无法获取锁
                redis_init.expire(lock, time_out)
                return True, identifier
            if redis_init.ttl(lock) in [-1, None]:
                redis_init.expire(lock, time_out)
            time.sleep(sleep_time)
        return False, ""

    @classmethod
    def release_lock(self, lock_name, identifier, config_dict=None):
        """
        :description: 释放分布式锁
        :param lock_name：锁定名称
        :param identifier: identifier
        :param config_dict：连接串配置
        :return bool
        :last_editors: yy
        """
        if share_config.get_value("is_pressure_test", False):  #是否进行压力测试
            return True
        lock = "lock:" + lock_name
        redis_init = self.init(config_dict=config_dict)
        pip = redis_init.pipeline(True)
        try:
            pip.watch(lock)
            lock_value = redis_init.get(lock)
            if not lock_value:
                return True
            if lock_value == identifier:
                pip.multi()
                pip.delete(lock)
                pip.execute()
                return True
            pip.unwatch()
            return False
        except Exception:
            pip.unwatch()
            return False
