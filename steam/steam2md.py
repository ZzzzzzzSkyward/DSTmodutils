import re
import argparse
from pathlib import Path

tags_one={'h1':'#','h2':'##','h3':'###','h4':'####','h5':'#####','h6':'######','*':'[*]','hr':'---'}
tags_two={'b':'**', 'i':'*', 'strike':'~','u':"",'spoiler':""}
tag_noparse='noparse'
tag_url='url='
tag_quote='quote='
tag_list='list'
tag_olist='olist'


def LoadFile(path) -> str:
    text=""
    with open(path,'r',encoding='utf-8') as f:
        text=f.read()
    return text

def ReadAhead(text):
    """
    读取无需转换的普通文本

    return : 普通字符串, 剩余bbcode文本
    """
    text_out=""
    for i in range(len(text)):
        c=text[i]
        if c != '[':
            text_out+=c
            continue
        else :
            return text_out,text[i:]
    return text_out,""

def BBCode2Markdown(text) -> str:
    text_out=""
    
    while text!="":
        text_process,text=ReadAhead(text)
        text_out+=text_process

        text_process,text=ParseTag(text)

        text_out+=text_process
    
    #整理换行
    text_out=NormalizeReturn(text_out)
    return text_out

def ParseTag(text):
    if text=="":
        return "",text

    """提取标签和剩余文本"""
    tag_end=text.find(']')
    #不完整标签处理
    if  tag_end==-1: return "[",text[1:]
    elif tag_end==1: return "[]",text[2:]
    #正常标签解析
    tag=text[1:tag_end]
    text=text[tag_end+1:]

    #特殊标签处理
    if tag[0]=='/':#结束标签
        return "",text
    elif tag==tag_noparse:#不解析标签
        end_noparse=text.find('/'+tag_noparse)
        return text[:end_noparse-1],text[end_noparse+len(tag_noparse)+2:]

    text_out=""
    text_process=""
    is_end=False

    """处理内层"""
    while  not is_end:
        text_temp,text=ReadAhead(text)
        text_process+=text_temp
        text_temp,text=ParseTag(text)
        if text_temp=='':#内层处理结束
            is_end=True
        text_process+=text_temp


    """处理本层"""
    if tag in tags_one:
        padding=tags_one[tag]+" "
        text_process=padding+text_process
        #标题不允许换行
        if tag[0]=='h':
            text_process=text_process.replace('\n','')

    elif tag in tags_two:
        padding=tags_two[tag]
        text_process= padding+text_process+padding

    elif tag.find('=') ==3:
        url=tag[4:]
        url_name=text_process
        text_process=f'[{url_name}]({url})'
    
    elif tag.find('=') ==5:
        quote_name=tag[6:]
        quote_text=text_process
        text_process=f'> {quote_text}      ----{quote_name}'
    
    elif tag==tag_list:
        padding="\n"
        text_process=text_process.replace('[*]',"-")
        text_process=padding+text_process+padding

    elif tag==tag_olist:
        padding="\n"
        count=text_process.count('[*]')
        for i in range(count):
            text_process=text_process.replace('[*]',str(i+1)+'.',1)
        text_process=padding+text_process+padding

    text_out+=text_process
    return text_out,text


def NormalizeReturn(text):
    expand_return=re.compile('\n+')
    text=expand_return.sub('\n',text)
    expand_return=re.compile('\n')
    text=expand_return.sub('\n\n',text)

    return text

def parsearg():
    parser=argparse.ArgumentParser()
    parser.add_argument('-i','--input',required=True,help="输入文件路径")
    parser.add_argument('-o','--output',default=None,help="输出文件路径")

    return parser.parse_args()

if __name__ == "__main__":
    args=parsearg()
    input=Path(args.input)
    bbcode=LoadFile(input)
    markdown=args.output if args.output else input.stem+".md"
    with open(markdown,'w') as f:
        f.write(BBCode2Markdown(bbcode))