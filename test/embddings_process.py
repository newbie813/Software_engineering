import pickle
import numpy as np
from gensim.models import KeyedVectors


def save_word_vectors_as_binary(input_path, output_path):
    """
    将词向量文件保存为二进制文件。

    参数:
    input_path (str): 输入的词向量文件路径（文本格式）。
    output_path (str): 输出的词向量文件路径（二进制格式）。
    """
    word_vectors = KeyedVectors.load_word2vec_format(input_path, binary=False)
    word_vectors.init_sims(replace=True)
    word_vectors.save(output_path)


def build_new_dictionary_and_vectors(input_vec_path, input_word_path, output_vec_path, output_word_path):
    """
    构建新的词典和词向量矩阵。

    参数:
    input_vec_path (str): 输入的词向量文件路径（二进制格式）。
    input_word_path (str): 输入的词典文件路径（文本格式）。
    output_vec_path (str): 输出的词向量矩阵文件路径（pickle格式）。
    output_word_path (str): 输出的词典文件路径（pickle格式）。
    """
    model = KeyedVectors.load(input_vec_path, mmap='r')

    with open(input_word_path, 'r') as file:
        total_words = eval(file.read())

    special_tokens = ['PAD', 'SOS', 'EOS', 'UNK']
    word_dict = special_tokens.copy()

    fail_words = []
    rng = np.random.RandomState(None)
    special_embeddings = {
        'PAD': np.zeros(shape=(300,)),
        'UNK': rng.uniform(-0.25, 0.25, size=(300,)),
        'SOS': rng.uniform(-0.25, 0.25, size=(300,)),
        'EOS': rng.uniform(-0.25, 0.25, size=(300,))
    }

    word_vectors = [special_embeddings[token] for token in special_tokens]

    for word in total_words:
        try:
            word_vectors.append(model[word])
            word_dict.append(word)
        except KeyError:
            fail_words.append(word)

    word_vectors = np.array(word_vectors)
    word_dict = {word: idx for idx, word in enumerate(word_dict)}

    with open(output_vec_path, 'wb') as file:
        pickle.dump(word_vectors, file)

    with open(output_word_path, 'wb') as file:
        pickle.dump(word_dict, file)

    print("词典和词向量构建完成。")


def get_word_index(type, text, word_dict):
    """
    获取词在词典中的位置。

    参数:
    type (str): 文本类型，可以是 'code' 或 'text'。
    text (list): 需要处理的文本列表。
    word_dict (dict): 词典。

    返回:
    list: 词在词典中的位置列表。
    """
    indices = []
    if type == 'code':
        indices.append(1)  # SOS_ID
        len_text = len(text)
        if len_text + 1 < 350:
            if len_text == 1 and text[0] == '-1000':
                indices.append(2)  # EOS_ID
            else:
                indices.extend(word_dict.get(word, word_dict['UNK']) for word in text)
                indices.append(2)  # EOS_ID
        else:
            indices.extend(word_dict.get(text[i], word_dict['UNK']) for i in range(348))
            indices.append(2)  # EOS_ID
    else:
        if len(text) == 0 or text[0] == '-10000':
            indices.append(0)  # PAD_ID
        else:
            indices.extend(word_dict.get(word, word_dict['UNK']) for word in text)

    return indices


def serialize_corpus(word_dict_path, input_corpus_path, output_corpus_path):
    """
    将训练、测试、验证语料序列化。

    参数:
    word_dict_path (str): 词典文件路径（pickle格式）。
    input_corpus_path (str): 输入的语料文件路径（文本格式）。
    output_corpus_path (str): 输出的序列化语料文件路径（pickle格式）。
    """
    with open(word_dict_path, 'rb') as file:
        word_dict = pickle.load(file)

    with open(input_corpus_path, 'r') as file:
        corpus = eval(file.read())

    total_data = []

    for entry in corpus:
        qid = entry[0]
        Si_word_list = get_word_index('text', entry[1][0], word_dict)
        Si1_word_list = get_word_index('text', entry[1][1], word_dict)
        tokenized_code = get_word_index('code', entry[2][0], word_dict)
        query_word_list = get_word_index('text', entry[3], word_dict)

        Si_word_list = (Si_word_list[:100] + [0] * (100 - len(Si_word_list)))[:100]
        Si1_word_list = (Si1_word_list[:100] + [0] * (100 - len(Si1_word_list)))[:100]
        tokenized_code = (tokenized_code[:350] + [0] * (350 - len(tokenized_code)))[:350]
        query_word_list = (query_word_list[:25] + [0] * (25 - len(query_word_list)))[:25]

        total_data.append([qid, [Si_word_list, Si1_word_list], [tokenized_code], query_word_list, 4, 0])

    with open(output_corpus_path, 'wb') as file:
        pickle.dump(total_data, file)

    print("语料序列化完成。")


if __name__ == '__main__':
    # 词向量文件路径
    python_vec_bin_path = '../hnn_process/embeddings/10_10/python_struc2vec.bin'
    sql_vec_bin_path = '../hnn_process/embeddings/10_8_embeddings/sql_struc2vec.bin'

    # 初始词典和词向量文件路径
    python_word_path = '../hnn_process/data/word_dict/python_word_vocab_dict.txt'
    python_word_vec_path = '../hnn_process/embeddings/python/python_word_vocab_final.pkl'
    python_word_dict_path = '../hnn_process/embeddings/python/python_word_dict_final.pkl'

    sql_word_path = '../hnn_process/data/word_dict/sql_word_vocab_dict.txt'
    sql_word_vec_path = '../hnn_process/embeddings/sql/sql_word_vocab_final.pkl'
    sql_word_dict_path = '../hnn_process/embeddings/sql/sql_word_dict_final.pkl'

    # 构建词典和词向量矩阵
    # build_new_dictionary_and_vectors(python_vec_bin_path, python_word_path, python_word_vec_path, python_word_dict_path)
    # build_new_dictionary_and_vectors(sql_vec_bin_path, sql_word_path, sql_word_vec_path, sql_word_dict_path)

    # 待处理语料地址
    new_sql_staqc_path = '../hnn_process/ulabel_data/staqc/sql_staqc_unlabled_data.txt'
    new_sql_large_path = '../hnn_process/ulabel_data/large_corpus/multiple/sql_large_multiple_unlable.txt'
    large_word_dict_sql_path = '../hnn_process/ulabel_data/sql_word_dict.txt'

    # 最终词典和词向量文件路径
    sql_final_word_vec_path = '../hnn_process/ulabel_data/large_corpus/sql_word_vocab_final.pkl'
    sql_final_word_dict_path = '../hnn_process/ulabel_data/large_corpus/sql_word_dict_final.pkl'

    # 序列化输出文件路径
    serialized_staqc_sql_path = '../hnn_process/ulabel_data/staqc/seri_sql_staqc_unlabled_data.pkl'
    serialized_large_sql_path = '../hnn_process/ulabel_data/large_corpus/multiple/seri_sql_large_multiple_unlable.pkl'

    # 序列化语料
    # serialize_corpus(sql_final_word_dict_path, new_sql_staqc_path, serialized_staqc_sql_path)
    # serialize_corpus(sql_final_word_dict_path, new_sql_large_path, serialized_large_sql_path)

    # Python部分
    new_python_staqc_path = '../hnn_process/ulabel_data/staqc/python_staqc_unlabled_data.txt'
    new_python_large_path = '../hnn_process/ulabel_data/large_corpus/multiple/python_large_multiple_unlable.txt'
    final_word_dict_python_path = '../hnn_process/ulabel_data/python_word_dict.txt'

    python_final_word_vec_path = '../hnn_process/ulabel_data/large_corpus/python_word_vocab_final.pkl'
    python_final_word_dict_path = '../hnn_process/ulabel_data/large_corpus/python_word_dict_final.pkl'

    serialized_staqc_python_path = '../hnn_process/ulabel_data/staqc/seri_python_staqc_unlabled_data.pkl'
    serialized_large_python_path = '../hnn_process/ulabel_data/large_corpus/multiple/seri_python_large_multiple_unlable.pkl'

    # 序列化语料
    # serialize_corpus(python_final_word_dict_path, new_python_staqc_path, serialized_staqc_python_path)
    serialize_corpus(python_final_word_dict_path, new_python_large_path, serialized_large_python_path)

    print('序列化完毕')
