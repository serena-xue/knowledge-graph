# 初步入库操作
import pandas as pd

import pandas as pd
from py2neo import Node,Relationship,Graph,NodeMatcher,RelationshipMatcher
import re


# 创建节点
def create_node(m_graph, m_label, m_attrs):
    m_n = "_.name="+"\'"+m_attrs['name']+"\'"
    matcher = NodeMatcher(m_graph)
    re_value = matcher.match(m_label).where(m_n).first()
    print(m_attrs)
    if re_value is None:
        m_mode = Node(m_label, **m_attrs)
        w = m_attrs['name']
        m_mode['w'] = w
        n = graph.create(m_mode)
        return n
    return None


# 查询节点
def match_node(m_graph, m_label, m_attrs):
    m_n = "_.name="+"\'" + m_attrs['name'] + "\'"
    matcher = NodeMatcher(m_graph)
    re_value = matcher.match(m_label).where(m_n).first()
    return re_value


# 创建关系
def create_relationship(m_graph, m_label1, m_attrs1, m_label2, m_attrs2, m_r_name):
    reValue1 = match_node(m_graph, m_label1, m_attrs1)
    reValue2 = match_node(m_graph, m_label2, m_attrs2)
    if reValue1 is None or reValue2 is None:
        return False

    m_r = Relationship(reValue1, m_r_name, reValue2)
    m_r['type'] = m_r_name
    print(m_r_name)
    n = graph.create(m_r)
    return n


graph = Graph("http://127.0.0.1:7474", auth=("neo4j", "123456"))


def get_entity():
    df = pd.read_csv("./三元组.csv")
    df.dropna(axis=0, how='any', inplace=True)
    entity = set(df['subject'].values)
    tail = set(df['object'].values)
    entity = entity.union(tail)
    return entity


# 根据实体和关系生成知识图谱
def to_neo4jgz():
    # 连接neo4j
    # 加载数据
    entity = get_entity()
    relation = pd.read_csv("./三元组.csv")
    relation.dropna(axis=0, how='any', inplace=True)
    # 创建实体
    label = "entity"
    for j in entity:
        # j=j.replace('‘','').replace("“","").replace("）","").replace("（","").replace('.',"")
        try:
            attr = {"name": j}
            create_node(graph, label, attr)
        except Exception as e:
            print(e.args)
            continue

    # 创建关系
    for i, j in relation.iterrows():
        try:
            attr1 = {"name": j['subject']}
            attr2 = {"name": j['object']}
            m_r_name = j['relation']
            reValue = create_relationship(graph, label, attr1, label, attr2, m_r_name)
        except Exception as e:
            continue


if __name__ == '__main__':
    print('graph 连接成功，开始清库')
    graph.delete_all()
    print('graph 清库成功')
    # 导入
    to_neo4jgz()

