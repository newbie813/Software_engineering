import pickle
from collections import Counter


def load_pickle(filename):
    """
    从文件中加载pickle数据。

    参数:
    filename (str): 文件路径。

    返回:
    object: 加载的pickle数据。
    """
    with open(filename, 'rb') as file:
        data = pickle.load(file, encoding='iso-8859-1')
    return data


def split_data(total_data, qids):
    """
    根据qids将数据分为单一和多重两部分。

    参数:
    total_data (list): 总数据。
    qids (list): qid列表。

    返回:
    tuple: 单一数据和多重数据。
    """
    qid_counts = Counter(qids)
    single_data = []
    multiple_data = []

    for data in total_data:
        if qid_counts[data[0][0]] == 1:
            single_data.append(data)
        else:
            multiple_data.append(data)

    return single_data, multiple_data


def process_staqc_data(filepath, single_save_path, multiple_save_path):
    """
    处理staqc数据，将其分为单一和多重两部分并保存。

    参数:
    filepath (str): 输入文件路径。
    single_save_path (str): 单一数据保存路径。
    multiple_save_path (str): 多重数据保存路径。
    """
    with open(filepath, 'r') as file:
        total_data = eval(file.read())

    qids = [data[0][0] for data in total_data]
    single_data, multiple_data = split_data(total_data, qids)

    with open(single_save_path, "w") as file:
        file.write(str(single_data))
    with open(multiple_save_path, "w") as file:
        file.write(str(multiple_data))


def process_large_data(filepath, single_save_path, multiple_save_path):
    """
    处理large数据，将其分为单一和多重两部分并保存。

    参数:
    filepath (str): 输入文件路径。
    single_save_path (str): 单一数据保存路径。
    multiple_save_path (str): 多重数据保存路径。
    """
    total_data = load_pickle(filepath)
    qids = [data[0][0] for data in total_data]
    single_data, multiple_data = split_data(total_data, qids)

    with open(single_save_path, 'wb') as file:
        pickle.dump(single_data, file)
    with open(multiple_save_path, 'wb') as file:
        pickle.dump(multiple_data, file)


def convert_single_unlabeled_to_labeled(input_path, output_path):
    """
    将单一未标记数据转换为标记数据。

    参数:
    input_path (str): 输入文件路径。
    output_path (str): 输出文件路径。
    """
    total_data = load_pickle(input_path)
    labeled_data = [[data[0], 1] for data in total_data]
    sorted_data = sorted(labeled_data, key=lambda x: (x[0], x[1]))

    with open(output_path, "w") as file:
        file.write(str(sorted_data))


if __name__ == "__main__":
    staqc_python_path = './ulabel_data/python_staqc_qid2index_blocks_unlabeled.txt'
    staqc_python_single_save = './ulabel_data/staqc/single/python_staqc_single.txt'
    staqc_python_multiple_save = './ulabel_data/staqc/multiple/python_staqc_multiple.txt'
    process_staqc_data(staqc_python_path, staqc_python_single_save, staqc_python_multiple_save)

    staqc_sql_path = './ulabel_data/sql_staqc_qid2index_blocks_unlabeled.txt'
    staqc_sql_single_save = './ulabel_data/staqc/single/sql_staqc_single.txt'
    staqc_sql_multiple_save = './ulabel_data/staqc/multiple/sql_staqc_multiple.txt'
    process_staqc_data(staqc_sql_path, staqc_sql_single_save, staqc_sql_multiple_save)

    large_python_path = './ulabel_data/python_codedb_qid2index_blocks_unlabeled.pickle'
    large_python_single_save = './ulabel_data/large_corpus/single/python_large_single.pickle'
    large_python_multiple_save = './ulabel_data/large_corpus/multiple/python_large_multiple.pickle'
    process_large_data(large_python_path, large_python_single_save, large_python_multiple_save)

    large_sql_path = './ulabel_data/sql_codedb_qid2index_blocks_unlabeled.pickle'
    large_sql_single_save = './ulabel_data/large_corpus/single/sql_large_single.pickle'
    large_sql_multiple_save = './ulabel_data/large_corpus/multiple/sql_large_multiple.pickle'
    process_large_data(large_sql_path, large_sql_single_save, large_sql_multiple_save)

    large_sql_single_label_save = './ulabel_data/large_corpus/single/sql_large_single_label.txt'
    large_python_single_label_save = './ulabel_data/large_corpus/single/python_large_single_label.txt'
    convert_single_unlabeled_to_labeled(large_sql_single_save, large_sql_single_label_save)
    convert_single_unlabeled_to_labeled(large_python_single_save, large_python_single_label_save)