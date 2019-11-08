from pyhanlp import *

file_name = "D:\\Github\\KnowledgeGraph\\nlp\\MilitaryCorpus.json"
# print(HanLP.segment("今天开心了吗？"))
with open(file_name, 'r', encoding='utf-8') as write_file_obj:
    print(HanLP.segment(write_file_obj.read()))
