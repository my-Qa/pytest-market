import pymysql
from conf.operationConfig import OperationConfig
from common.recordlog import logs

conf = OperationConfig()


class ConnectMysql:

    def __init__(self):
        self.conn = None
        self.cursor = None
        mysql_conf = {
            'host': conf.get_section_mysql('host'),
            'port': int(conf.get_section_mysql('port')),
            'user': conf.get_section_mysql('username'),
            'password': conf.get_section_mysql('password'),
            'database': conf.get_section_mysql('database')
        }

        try:
            self.conn = pymysql.connect(**mysql_conf, charset='utf8')
            # cursor=pymysql.cursors.DictCursor,将数据库表字段显示，以key-value形式展示
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            logs.info("""成功连接到mysql---
            host：{host}
            port：{port}
            db：{database}
            """.format(**mysql_conf))
        except Exception as e:
            logs.error(f"连接MySQL失败，请检查conf/config.ini中的[MYSQL]配置：{e}")

    def close(self):
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None
        if self.conn is not None:
            self.conn.close()
            self.conn = None
        return True

    def query_all(self, sql):
        if self.cursor is None:
            logs.error('MySQL连接不可用，无法执行查询，请检查[MYSQL]配置')
            return None
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            values = [list(row.values()) for row in res]
            # 查询到数据返回全部行，无数据返回None，供断言判断
            return values if values else None
        except Exception as e:
            logs.error(e)
        finally:
            self.close()

    def delete(self, sql):
        if self.cursor is None:
            logs.error('MySQL连接不可用，无法执行删除，请检查[MYSQL]配置')
            return None
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            logs.info('删除成功')
        except Exception as e:
            logs.error(e)
        finally:
            self.close()
