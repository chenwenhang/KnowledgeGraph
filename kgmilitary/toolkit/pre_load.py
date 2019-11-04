# -*- coding: utf-8 -*-
import thulac
import sys
import csv
import os

sys.path.append("..")

from Model.neo4j_models import Neo4j_Handle

filePath = os.getcwd()

# 加载用户字典
thuFactory = thulac.thulac(user_dict=filePath + "/toolkit/userDict.txt")
print('--init thulac()--')

# 预加载Neo4j图数据库
neo4jconn = Neo4j_Handle()
neo4jconn.connectDB()
print('--Neo4j connecting--')

# 加载预定义单词类型
domain_ner_dict = {}
with open(filePath + '/toolkit/domainDict.csv', 'r', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        # 实体 类型代码
        domain_ner_dict[str(row[0])] = int(row[1])
print('--Load Domain Dictionary...--!')
