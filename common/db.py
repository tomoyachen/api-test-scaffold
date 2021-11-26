import pymysql
import redis
from common.config import Config
import logging
import allure

log = logging.getLogger()


class Mysql:
    def __init__(self, mysql_config=None):
        mysql_config = mysql_config if mysql_config else Config.get_config("mysql_config")
        self.conn = pymysql.connect(**mysql_config, autocommit = False)
        self.cur = self.conn.cursor(cursor = pymysql.cursors.DictCursor)

    @allure.step("Mysql Select")
    def select(self, sql) -> list:
        if "select " in sql:
            if " where " in sql:
                self.cur.execute(sql)
                results = self.cur.fetchall()
                log.info(f'SQL 查询: {sql}, 查询结果: {results}')
                return results
            else:
                log.info(f"SQL 查询: {sql}, 仅允许携带 where 条件执行")
        else:
            log.info(f"SQL 查询: {sql}, 这不是一条 select 语句")

    @allure.step("Mysql Select")
    def select_one(self, sql) -> dict:
        if "select " in sql:
            if " where " in sql:
                self.cur.execute(sql)
                result = self.cur.fetchone()
                log.info(f'SQL 查询: {sql}, 查询结果: {result}')
                return result
            else:
                log.info(f"SQL 查询: {sql}, 仅允许携带 where 条件执行")
        else:
            log.info(f"SQL 查询: {sql}, 这不是一条 select 语句")

    @allure.step("Mysql Update")
    def update_one(self, sql) -> int:
        if "update " in sql:
            if " where " in sql:
                count = self.cur.execute(sql)
                if count <= 1:
                    self.conn.commit()
                    log.info(f'SQL 更新: {sql}, 影响行数: {count}')
                    return count
                else:
                    log.info(f"SQL 更新: {sql}, 仅允许更新 1 条记录")
            else:
                log.info(f"SQL 更新: {sql}, 仅允许携带 where 条件执行")
        else:
            log.info(f"SQL 更新: {sql}, 这不是一条 update 语句")

    def close(self):
        self.cur.close()
        self.conn.close()


class Redis:
    def __init__(self, redis_config=None):
        redis_config = redis_config if redis_config else Config.get_config("redis_config")
        self.host = redis_config["host"]
        self.port = redis_config["port"]
        self.password = redis_config["password"]
        self.db = redis_config["db"]
        self.pool = redis.ConnectionPool(host=self.host, port=self.port, password=self.password, db=self.db)
        self.conn = redis.Redis(connection_pool = self.pool)

    @allure.step("Redis Set")
    def set_value(self, name, value):
        self.conn.set(name, value, ex=60)

    @allure.step("Redis Get")
    def get_value(self, name):
        try:
            value_as_bytes = self.conn.get(name)
            return value_as_bytes.decode()
        except Exception:
            pass

    @allure.step("Redis Get")
    def get_names(self, name = '*'):
        keys_as_bytes = self.conn.keys(pattern=name)
        keys = [item.decode() for item in keys_as_bytes]
        return keys

    @allure.step("Redis Hash Set")
    def set_hash_value(self, name, key, value):
        self.conn.set(name, key, value, ex=60)

    @allure.step("Redis Hash Get")
    def get_hash_value(self, name, key):
        try:
            value_as_bytes = self.conn.hget(name, key)
            return value_as_bytes.decode()
        except Exception:
            pass

    @allure.step("Redis Hash Get")
    def get_hash_keys(self, name):
        keys_as_bytes = self.conn.hkeys(name)
        keys = [item.decode() for item in keys_as_bytes]
        return keys
