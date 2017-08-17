# -*- coding:utf8 -*-

from __future__ import print_function
import codecs
import re
import json

def get_pairs(path):
    with codecs.open(path, encoding='utf8') as fp:
        text = fp.read()
        text = str(text.encode('utf8'))
        pair_list = re.findall(r'<category>(.*?)</category>', text, re.S)
        json_data = {}
        num = 0
        for pair in pair_list:
            pair = pair.strip().replace('<pattern>', '')
            pair = pair.strip().replace('</pattern>', '\t')
            pair = pair.strip().replace('<template>', '')
            pair = pair.strip().replace('</template>', '')
            pair = pair.strip().split()
            json_data['id'] = num
            json_data['question'] = pair[0]
            json_data['utterance'] = pair[1]
            num += 1
            yield json.dumps(json_data)

def save_pairs(data_path, save_path):
    with open(save_path, 'a') as fw:
        for json_data in get_pairs(data_path):
            fw.write(json_data+'\n')

def main():
    data_path = '../corpus/pairs/main.aiml'
    save_path = '../corpus/pairs/tk_pairs.json'
    save_pairs(data_path, save_path)

if __name__ == '__main__':
    main()