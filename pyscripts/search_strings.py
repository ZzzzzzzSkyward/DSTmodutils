import json
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import polib
import os
db={}
lookup={}
banlist=["STRINGS","CHARACTERS","NAMES","DESCRIBE"]
sentences = []
tfidf_vectorizer=None
tfidf_matrix=None
# 加载数据库
def loaddb():
    global db
    global tfidf_vectorizer
    global tfidf_matrix
    if not os.path.exists('chinese_s.po'):
        messagebox.showerror('错误','找不到chinese_s.po')
        exit(0)
    pofile=polib.pofile('chinese_s.po')
    db={i.msgctxt:i.msgstr for i in pofile}
    # 将句子按照.和_分隔符划分
    for sentence in db.keys():
        st=preprocess_input(sentence)
        lookup[st]=sentence
        sentences.append(st)

    # 计算 TF-IDF
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(sentences)

def preprocess_input(sentence):
    # 将输入的句子按照.和_分隔符划分
    tokens=sentence.split('.')
    subtokens=[t.split('_') for t in tokens]
    # 展平子标记列表
    flat_subtokens = [subtoken for sublist in subtokens for subtoken in sublist]
    flat_subtokens=[i for i in flat_subtokens if i not in banlist]
    return " ".join(flat_subtokens)
def get_translation(key):
    if key in db:
        return db[key]
    if key in lookup:
        return get_translation(lookup[key])
    return ""
def get_key(key):
    if key in lookup:
        return lookup[key]
    return key
import tkinter as tk
import tkinter.font as tf

length = 20
output_text=None
class MyApp:
    def __init__(self, root):
        self.root = root
        self.font=tf.Font(family="等线",size=14)
        self.root.title("相似句子检索")
        self.root.geometry("400x400")
        # 创建文本框
        self.text_box = scrolledtext.ScrolledText(self.root, width=100, height=3,font=self.font)
        self.text_box.pack(padx=0,pady=10)
        # 向列表中添加文本框
        self.output_text = scrolledtext.ScrolledText(self.root, width=100, height=20,font=self.font)
        self.output_text.pack(padx=0,pady=10)

inited=False
def retrieve_similar_sentences(event):
    global inited
    if not inited:
        loaddb()
        inited=True
    input_sentence = input_text.get("1.0", "end-1c").strip()
    if input_sentence:
        input_tokens = preprocess_input(input_sentence)
        
        # 计算输入句子的 TF-IDF
        input_tfidf = tfidf_vectorizer.transform([input_tokens])

        # 计算输入句子与数据库中句子的相似度
        similarities = cosine_similarity(input_tfidf, tfidf_matrix)

        # 获取相似度最高的前10个句子
        similar_indices = similarities.argsort()[0][-length:][::-1]

        # 在输出文本框中展示相似句子及其翻译
        lasti=-1
        output_text.delete('1.0', tk.END)
        for i, idx in enumerate(similar_indices):
            similar_sentence = get_key(sentences[idx])
            translation = get_translation(similar_sentence)
            similarity_score = similarities[0][idx]  # 获取相似度值
            if similarity_score>0.01:
                output_text.insert(tk.END, f"代码={similar_sentence}\n翻译={translation}\n\n")
            else:
                lasti=i
                break
        #too slow!!!
        if lasti>=0 and len(input_tokens)<40:
            results=retrieve_similar_sentences_edit(input_tokens,length-lasti)
            output_text.delete('1.0', tk.END)
            for i in range(i,length):
                if i<len(results):
                    similar_sentence = get_key(results[i][1])
                    translation = get_translation(similar_sentence)
                    output_text.insert(tk.END, f"代码={similar_sentence}\n翻译={translation}\n\n")

            
def remove_space(s):
    return s.replace(" ", "")
def edit_distance_ends_only(str1, str2,threshold=100):
    m, n = len(str1), len(str2)

    # 创建一个二维数组来存储编辑距离
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 初始化第一行和第一列
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # 动态规划计算编辑距离
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # 只能在开头或结尾插入或删除
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1])
                
    #print(str2,threshold,dp[m][n])
    return dp[m][n]
import heapq

def retrieve_similar_sentences_edit(input_sentence, k=10):
    input_sentence_processed = input_sentence
    max_heap = []

    for sentence in db:
        processed_sentence = sentence
        similarity_score = edit_distance_ends_only(input_sentence_processed, processed_sentence, get_threshold(max_heap, k))
        expected_edit=abs(len(input_sentence_processed)-len(processed_sentence))+1
        score=similarity_score
        #print(processed_sentence,score,get_threshold(max_heap, k))
        # 如果堆中句子不足k个，或者当前句子的相似度比堆中最大相似度还大，则加入堆
        if score <= get_threshold(max_heap, k):
            heapq.heappush(max_heap, (-score, sentence))
            #print("new",processed_sentence,get_threshold(max_heap, k))
            
        if len(max_heap)>k:
            heapq.heappop(max_heap)

    # 反转堆中元素，使得相似度最大的句子排在堆顶
    max_heap.sort(reverse=True)

    return max_heap

def get_threshold(heap, k):
    if len(heap) ==0:
        return 100
    return -heap[0][0]

root = tk.Tk()
app = MyApp(root)
# 创建输入文本框
input_text = app.text_box
output_text=app.output_text
# 监听文本框内容变化事件
def on_key_release(event):
    # 每次键释放事件被触发时，取消先前的定时器（如果存在）
    if hasattr(on_key_release, "timer"):
        root.after_cancel(on_key_release.timer)
    # 设置一个新的定时器，在0.5秒后调用处理函数
    on_key_release.timer = root.after(500, retrieve_similar_sentences, event)

input_text.bind("<KeyRelease>", on_key_release)
if __name__=='__main__':
    root.mainloop()