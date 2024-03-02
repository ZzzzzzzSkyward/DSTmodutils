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
sentences_trans = []
tfidf_vectorizer=None
tfidf_matrix=None
tfidf_vectorizer_trans=None
tfidf_matrix_trans=None
reverse_index={}
# 加载数据库
def loaddb():
    global db
    global tfidf_vectorizer
    global tfidf_vectorizer_trans
    global tfidf_matrix
    global tfidf_matrix_trans
    if not os.path.exists('chinese_s.po'):
        messagebox.showerror('错误','找不到chinese_s.po')
        exit(0)
    pofile=polib.pofile('chinese_s.po')
    db={i.msgctxt:i.msgstr for i in pofile}
    # 将句子按照.和_分隔符划分
    cached={}
    for sentence in list(db.keys()):
        st=preprocess_input(sentence)
        tr=preprocess_input(db[sentence])
        if len(st)==0 or len(tr)==0:
            del db[sentence]
            continue
        elif sentence!=st:
            lookup[st]=sentence
        sentences.append(st)
        if tr not in cached:
            sentences_trans.append(tr)
            cached[tr]=True
            reverse_index[tr]=[sentence]
        else:
            reverse_index[tr].append(sentence)
    # 计算 TF-IDF
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_vectorizer_trans = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(sentences)
    tfidf_matrix_trans = tfidf_vectorizer_trans.fit_transform(sentences_trans)

def preprocess_input(sentence):
    # 将输入的句子按照.和_分隔符划分
    tokens=sentence.split('.')
    subtokens=[t.split('_') for t in tokens]
    # 展平子标记列表
    flat_subtokens = [subtoken for sublist in subtokens for subtoken in sublist]
    flat_subtokens=[i for i in flat_subtokens if i not in banlist]
    #分割\n
    s=" ".join(flat_subtokens)
    return s.replace('\n',' ').replace('\r',' ').upper()

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
oldst=""
import time
# 全局变量，用于存储上次调用的时间
last_call_time = None

# 定义函数，用于测量调用的耗时并打印
def measure_time():
    return
    global last_call_time
    
    # 获取当前时间
    current_time = time.time()
    
    # 如果是第一次调用，则无法计算上次调用的耗时
    if last_call_time is not None:
        # 计算距离上次调用的时间间隔
        time_elapsed = current_time - last_call_time
        print("距离上次调用的耗时:", time_elapsed, "秒")
    else:
        print("计时器初始化")
    
    # 更新上次调用的时间为当前时间
    last_call_time = current_time
def retrieve_tf_idf(candidate,lasti,cached):
    results=[]
    # 计算输入句子的 TF-IDF
    input_tfidf = tfidf_vectorizer.transform(candidate)

    # 计算输入句子与数据库中句子的相似度
    similarities = cosine_similarity(input_tfidf, tfidf_matrix)

    # 获取相似度最高的前10个句子
    similar_indices = similarities.argsort()[0][lasti-length:][::-1]
    # 在输出文本框中展示相似句子及其翻译
    for i, idx in enumerate(similar_indices):
        similar_sentence = get_key(sentences[idx])
        translation = get_translation(similar_sentence)
        similarity_score = similarities[0][idx]  # 获取相似度值
        if lasti==length:
            break
        if similarity_score<0.01:
            break
        if similar_sentence not in cached:
            results.append(similar_sentence)
            cached[similar_sentence]=True
            lasti+=1
    return results,lasti
def retrieve_similar_sentences(event):
    measure_time()
    global oldst
    global inited
    if not inited:
        loaddb()
        inited=True
    input_sentence = input_text.get("1.0", "end-1c").strip()
    input_tokens = preprocess_input(input_sentence)
    measure_time()
    if input_tokens and input_tokens!=oldst:
        output_text.delete('1.0', tk.END)
        oldst=input_tokens
        lasti=0
        candidate=[input_tokens]
        results=[]
        cached={}
        results_special={}
        results_special[False]=[]
        if input_tokens in db:
            translation=db[input_tokens]
            results_special[True]=translation
            cached[input_tokens]=True
            lasti+=1
        elif input_sentence in db:
            translation=db[input_sentence]
            results_special[True]=translation
            cached[input_sentence]=True
            lasti+=1
        else:
            for i in db:
                translation=db[i]
                trans=preprocess_input(translation)
                if trans==input_tokens and i not in cached:
                    results_special[False].append(i)
                    cached[i]=True
                    candidate.append(trans)
                    lasti+=1
        if lasti<length:
            code_or_trans=Code_Or_Trans(input_sentence)
            doc=[" ".join(candidate)]
            measure_time()
            if code_or_trans:
                res,lasti=retrieve_tf_idf(candidate,lasti,cached)
                results.extend(res)
            else:
                # 计算输入句子的 TF-IDF
                input_tfidf = tfidf_vectorizer_trans.transform(doc)

                # 计算输入句子与数据库中句子的相似度
                similarities = cosine_similarity(input_tfidf, tfidf_matrix_trans)

                # 获取相似度最高的前10个句子
                similar_indices = similarities.argsort()[0][lasti-length:][::-1]
                matched=[]
                # 在输出文本框中展示相似句子及其翻译
                for i, idx in enumerate(similar_indices):
                    similar_trans = sentences_trans[idx]
                    similarity_score = similarities[0][idx]  # 获取相似度值
                    if similarity_score<0.01:
                        break
                    matched.extend(reverse_index[similar_trans])
                if len(matched)>0:
                    for i in matched:
                        if lasti==length:
                            break
                        if i not in cached:
                            cached[i]=True
                            results.append(i)
                            lasti+=1
                    match_doc=[preprocess_input(i) for i in matched]
                    res,lasti=retrieve_tf_idf(match_doc,lasti,cached)
                    results.extend(res)
            measure_time()

            #too slow!!!
            if lasti<length and len(input_tokens)<40:
                result=retrieve_similar_sentences_edit(input_tokens,length-lasti)
                for i in result:
                    similar_sentence = get_key(i[1])
                    if similar_sentence not in cached:
                        results.append(similar_sentence)
                        cached[similar_sentence]=True
                        lasti+=1
            measure_time()
            

        if True in results_special:
            translation=results_special[True]
            output_text.insert(tk.END, f"翻译={translation}\n\n")
        for i in results_special[False]:
            output_text.insert(tk.END, f"代码={i}\n\n")
        idx=1
        for i in results:
            similar_sentence,translation=i,get_translation(i)
            output_text.insert(tk.END, f"{idx}.代码{similar_sentence}\n翻译={translation}\n\n")
            idx+=1
            
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
def Code_Or_Trans(text):
    count_code=0
    count_trans=0
    for i in text:
        if 'A'<=i<='Z' or i=='_' or i=='.':
            count_code+=1
        else:
            count_trans+=1
    return count_code>=count_trans
def retrieve_similar_sentences_edit(input_sentence, k=10):
    input_sentence_processed = input_sentence
    max_heap = []
    code_or_trans=Code_Or_Trans(input_sentence)
    for sentence in db:
        processed_sentence = sentence
        similarity_score = edit_distance_ends_only(input_sentence_processed, processed_sentence, get_threshold(max_heap, k)) if code_or_trans else edit_distance_ends_only(input_sentence_processed,db[sentence], get_threshold(max_heap, k))
        #expected_edit=abs(len(input_sentence_processed)-len(processed_sentence))+1
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