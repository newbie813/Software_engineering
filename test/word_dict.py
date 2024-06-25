import pickle

def build_vocabulary(corpus1, corpus2):
    """
    构建词汇表，从两个语料库中提取唯一单词集合。

    参数:
    corpus1 (list): 第一个语料库数据。
    corpus2 (list): 第二个语料库数据。

    返回:
    set: 包含来自两个语料库的唯一单词集合。
    """
    word_vocab = set()
    for corpus in [corpus1, corpus2]:
        for data in corpus:
            word_vocab.update(data[1][0])
            word_vocab.update(data[1][1])
            word_vocab.update(data[2][0])
            word_vocab.update(data[3])
    print(len(word_vocab))
    return word_vocab

def load_pickle_data(filename):
    """
    加载 pickle 文件中的数据。

    参数:
    filename (str): pickle 文件的文件路径。

    """
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data

def process_vocabulary_files(file1, file2, save_path):
    """
    处理词汇文件，创建一个新的词汇文件。

    参数:
    file1 (str): 第一个词汇文件的文件路径。
    file2 (str): 第二个词汇文件的文件路径。
    save_path (str): 保存新词汇文件的文件路径。
    """
    with open(file1, 'r') as f:
        total_data1 = set(eval(f.read()))
    with open(file2, 'r') as f:
        total_data2 = eval(f.read())

    word_set = build_vocabulary(total_data1, total_data2)

    excluded_words = total_data1.intersection(word_set)
    word_set = word_set - excluded_words

    print(len(total_data1))
    print(len(word_set))

    with open(save_path, 'w') as f:
        f.write(str(word_set))

if __name__ == "__main__":
    python_hnn_data = './data/python_hnn_data_teacher.txt'
    python_staqc_data = './data/staqc/python_staqc_data.txt'
    python_word_vocab_dict = './data/word_dict/python_word_vocab_dict.txt'

    sql_hnn_data = './data/sql_hnn_data_teacher.txt'
    sql_staqc_data = './data/staqc/sql_staqc_data.txt'
    sql_word_vocab_dict = './data/word_dict/sql_word_vocab_dict.txt'

    new_sql_staqc_data = './ulabel_data/staqc/sql_staqc_unlabled_data.txt'
    new_sql_large_data = './ulabel_data/large_corpus/multiple/sql_large_multiple_unlable.txt'
    large_sql_word_dict = './ulabel_data/sql_word_dict.txt'

    process_vocabulary_files(sql_word_vocab_dict, new_sql_large_data, large_sql_word_dict)