from sentence_parser import *
import re
import os
from time import time
from pprint import pprint
from  pyltp import SentenceSplitter, Segmentor, Postagger, Parser
from utils import clean_text
from collections import Counter


class TripleExtractor:
    def __init__(self):
        self.parser = LtpParser()

    '''文章分句处理, 切分长句，冒号，分号，感叹号等做切分标识'''

    def split_sents(self, content):
        return [sentence for sentence in re.split(r'[？?！!。；;：:\n\r]', content) if
                sentence and '北京银行' in sentence and len(sentence) < 300]

    '''利用语义角色标注,直接获取主谓宾三元组,基于A0,A1,A2'''

    def ruler1(self, words, postags, roles_dict, role_index):
        # words:['中国', '是', '一个', '自由', '、', '和平', '的', '国家']
        # postags:['ns', 'v', 'm', 'a', 'wp', 'a', 'u', 'n']
        # roles_dict:{1: {'A0': ['A0', 0, 0], 'A1': ['A1', 2, 7]}}
        # role_index:1
        v = words[role_index]  # 是
        role_info = roles_dict[role_index]
        if 'A0' in role_info.keys() and 'A1' in role_info.keys():
            s = ''.join([words[word_index] for word_index in range(role_info['A0'][1], role_info['A0'][2] + 1) if
                         postags[word_index][0] not in ['w', 'u', 'x'] and words[word_index]])
            o = ''.join([words[word_index] for word_index in range(role_info['A1'][1], role_info['A1'][2] + 1) if
                         postags[word_index][0] not in ['w', 'u', 'x'] and words[word_index]])
            if s and o:
                return '1', [s, v, o]
        # elif 'A0' in role_info:
        #     s = ''.join([words[word_index] for word_index in range(role_info['A0'][1], role_info['A0'][2] + 1) if
        #                  postags[word_index][0] not in ['w', 'u', 'x']])
        #     if s:
        #         return '2', [s, v]
        # elif 'A1' in role_info:
        #     o = ''.join([words[word_index] for word_index in range(role_info['A1'][1], role_info['A1'][2]+1) if
        #                  postags[word_index][0] not in ['w', 'u', 'x']])
        #     return '3', [v, o]
        return '4', []

    '''三元组抽取主函数'''

    def ruler2(self, words, postags, child_dict_list, roles_dict, arcs):
        # words:['中国', '是', '一个', '自由', '、', '和平', '的', '国家']
        # postags:['ns', 'v', 'm', 'a', 'wp', 'a', 'u', 'n']
        # child_dict_list:[{}, {'SBV': [0], 'VOB': [7]}, {}, {'COO': [5], 'RAD': [6]}, {}, {'WP': [4]}, {}, {'ATT': [2, 3]}]
        # roles_dict:{1: {'A0': ['A0', 0, 0], 'A1': ['A1', 2, 7]}}
        # arcs:[['SBV', '中国', 0, 'ns', '是', 1, 'v'], ['HED', '是', 1, 'v', 'Root', -1, 'n'], ['ATT', '一个', 2, 'm', '国家', 7, 'n'], ['ATT', '自由', 3, 'a', '国家', 7, 'n'], ['WP', '、', 4, 'wp', '和平', 5, 'a'], ['COO', '和平', 5, 'a', '自由', 3, 'a'], ['RAD', '的', 6, 'u', '自由', 3, 'a'], ['VOB', '国家', 7, 'n', '是', 1, 'v']]
        svos = []
        for index in range(len(postags)):  # [0,1,2,3,4,5,6,7]
            tmp = 1
            # 先借助语义角色标注的结果，进行三元组抽取
            if index in roles_dict:  # 1
                flag, triple = self.ruler1(words, postags, roles_dict, index)
                if flag == '1':
                    svos.append(triple)
                    tmp = 0
            if tmp == 1:
                # 如果语义角色标记为空，则使用依存句法进行抽取
                # if postags[index] == 'v':
                if postags[index]: # 是
                    # 抽取以谓词为中心的事实三元组
                    child_dict = child_dict_list[index]
                    # 主谓宾
                    # SBV:我送她一束花 (我 <– 送)
                    # VOB:我送她一束花 (送 –> 花)
                    if 'SBV' in child_dict and 'VOB' in child_dict:
                        r = words[index]
                        e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                        e2 = self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
                        svos.append([e1, r, e2])

                    # 定语后置，动宾关系
                    # ATT:红苹果 (红 <– 苹果)
                    relation = arcs[index][0]
                    head = arcs[index][2]
                    if relation == 'ATT':
                        if 'VOB' in child_dict:
                            e1 = self.complete_e(words, postags, child_dict_list, head - 1)
                            r = words[index]
                            e2 = self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
                            temp_string = r + e2
                            if temp_string == e1[:len(temp_string)]:
                                e1 = e1[len(temp_string):]
                            if temp_string not in e1:
                                svos.append([e1, r, e2])
                    # 含有介宾关系的主谓动补关系
                    # CMP:做完了作业 (做 –> 完)
                    # POB:在贸易区内 (在 –> 内)
                    if 'SBV' in child_dict and 'CMP' in child_dict:
                        e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                        cmp_index = child_dict['CMP'][0]
                        r = words[index] + words[cmp_index]
                        if 'POB' in child_dict_list[cmp_index]:
                            e2 = self.complete_e(words, postags, child_dict_list, child_dict_list[cmp_index]['POB'][0])
                            svos.append([e1, r, e2])
        return svos

    '''对找出的主语或者宾语进行扩展'''

    def complete_e(self, words, postags, child_dict_list, word_index):
        child_dict = child_dict_list[word_index]
        prefix = ''
        if 'ATT' in child_dict:
            for i in range(len(child_dict['ATT'])):
                prefix += self.complete_e(words, postags, child_dict_list, child_dict['ATT'][i])
        postfix = ''
        if postags[word_index] == 'v':
            if 'VOB' in child_dict:
                postfix += self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
            if 'SBV' in child_dict:
                prefix = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0]) + prefix

        return prefix + words[word_index] + postfix

    '''程序主控函数'''

    def triples_main(self, content):
        # sentences = self.split_sents(content)
        svos = []
        sentence = content
        # for sentence in sentences:
        words, postags, child_dict_list, roles_dict, arcs = self.parser.parser_main(sentence)
        svo = self.ruler2(words, postags, child_dict_list, roles_dict, arcs)
        svos += svo

        return svos


def test():
    extractor = TripleExtractor()
    contents = [
        '中国是一个自由、和平的国家',
        '他什么书都读',
        '在贸易区内,他完成了交易',
        '红色的苹果真好看',
        '我送她一朵花',
        '我做完了作业',
    ]
    # contents=open('C:\\Users\\86188\\Desktop\\new.txt',encoding='utf-8')
    for content in contents:
        print(extractor.triples_main(content))

# test()
