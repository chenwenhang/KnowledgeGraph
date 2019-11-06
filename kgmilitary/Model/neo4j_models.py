# -*- coding: utf-8 -*-
from py2neo import Graph, Node, Relationship, NodeMatcher


# 版本说明：Py2neo v4
class Neo4j_Handle():
    graph = None
    matcher = None

    def __init__(self):
        print("Neo4j Init ...")

    def connectDB(self):
        self.graph = Graph("bolt: // localhost:7687", username="neo4j", password="cwhwy2015gkjy!")
        self.matcher = NodeMatcher(self.graph)

    # 实体查询，用于命名实体识别
    def matchEntityItem(self, value):
        answer = self.graph.run("MATCH (entity1) WHERE entity1.name = \"" + value + "\" RETURN entity1").data()
        return answer

    # 实体查询
    def getEntityRelationbyEntity(self, value):
        # 查询实体：不考虑实体类型，只考虑关系方向
        answer = self.graph.run(
            "MATCH (entity1) - [rel] -> (entity2)  WHERE entity1.name = \"" + value + "\" RETURN rel,entity2").data()
        if (len(answer) == 0):
            # 查询实体：不考虑关系方向
            answer = self.graph.run(
                "MATCH (entity1) - [rel] - (entity2)  WHERE entity1.name = \"" + value + " \" RETURN rel,entity2").data()
        print(answer)
        return answer

    # 关系查询:实体1
    def findRelationByEntity1(self, entity1):
        answer = self.graph.run("MATCH (n1)- [rel] -> (n2) WHERE n1.name=\"" + entity1 + "\" RETURN n1,rel,n2").data()
        return answer

    # 关系查询：实体2
    def findRelationByEntity2(self, entity2):
        answer = self.graph.run("MATCH (n1)- [rel] -> (n2) WHERE n2.name=\"" + entity2 + "\"  RETURN n1,rel,n2").data()
        return answer

    # 关系查询：实体1+关系
    def findOtherEntities(self, entity, relation):
        answer = self.graph.run(
            "MATCH (n1)- [rel] -> (n2) WHERE n1.name=\"" + entity + "\" and  rel.name=\""
            + relation + "\" RETURN n1,rel,n2").data()
        return answer

    # 关系查询：关系+实体2
    def findOtherEntities2(self, entity, relation):
        answer = self.graph.run(
            "MATCH (n1)- [rel] -> (n2) WHERE n2.name=\"" + entity + "\" and  rel.name=\""
            + relation + "\" RETURN n1,rel,n2").data()
        return answer

    # 关系查询：实体1+实体2(注意Entity2的空格）
    def findRelationByEntities(self, entity1, entity2):
        answer = self.graph.run(
            "MATCH (n1)- [rel] -> (n2) WHERE n1.name=\"" + entity1 + "\" and  n2.name=\""
            + entity2 + "\" RETURN n1,rel,n2").data()
        return answer

    # 查询数据库中是否有对应的实体-关系匹配
    def findEntityRelation(self, entity1, relation, entity2):
        answer = self.graph.run(
            "MATCH (n1)- [rel] -> (n2) WHERE n1.name=\"" + entity1 + "\" and  n2.name=\""
            + entity2 + "\" and  rel.name=\""
            + relation + "\"  RETURN n1,rel,n2").data()
        return answer
