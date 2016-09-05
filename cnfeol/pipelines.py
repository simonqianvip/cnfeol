# -*- coding: utf-8 -*-
import json
import codecs
import logging
from scrapy import signals
from twisted.enterprise import adbapi
from datetime import datetime
import MySQLdb
import MySQLdb.cursors
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

logger = logging.getLogger(__name__)
class CnfeolPipeline(object):
    def process_item(self, item, spider):
        return item


class MySQLStoreCnfeolPipeline(object):
    """
    数据存储到mysql
    """
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        '''
        从settings文件加载属性
        :param settings:
        :return:
        '''
        dbargs = dict(
                host=settings['MYSQL_HOST'],
                db=settings['MYSQL_DBNAME'],
                user=settings['MYSQL_USER'],
                passwd=settings['MYSQL_PASSWD'],
                charset='utf8',
                cursorclass=MySQLdb.cursors.DictCursor,
                use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    # pipeline默认调用
    def process_item(self, item, spider):
        deferred = self.dbpool.runInteraction(self._do_insert, item, spider)
        deferred.addErrback(self._handle_error)
        # d.addBoth(lambda _: item)
        return deferred

    # 将每行更新或写入数据库中
    def _do_insert(self, conn, item, spider):
        """
        CREATE TABLE `cnfeol_info` (
          `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
          `pname` varchar(50) COMMENT "名称",
          `ptype` varchar(50) COMMENT '类型',
          `min_price` varchar(50)  COMMENT '最低价格',
          `max_price` VARCHAR(50)  COMMENT '最高价格',
          `pchange` VARCHAR(50)  COMMENT '涨跌',
          `punit` VARCHAR(50)  COMMENT '单位',
          `premark` VARCHAR(50)  COMMENT '备注',
          `pdate` VARCHAR(50)  COMMENT '日期',
          PRIMARY KEY (`id`)
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
        """

        conn.execute("""
                select * from cnfeol_info where pname = %s and ptype = %s and premark = %s and pdate = %s
        """, (item['name'],item['type'],item['remark'],item['date'] ))
        ret = conn.fetchone()

        if ret:
            logger.info('数据已存在')
        else:
            conn.execute("""
                    insert into cnfeol_info(pname, ptype, min_price, max_price,pchange,punit,premark,pdate)
                    values(%s, %s, %s, %s,%s, %s, %s, %s)
                    """, (item['name'],item['type'] ,item['min_price'] ,item['max_price'],item['change'],item['unit'],item['remark'],item['date']))
            logger.info('insert into is success')

    def _handle_error(self, failue):
        logger.error(failue)