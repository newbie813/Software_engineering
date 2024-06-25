import pickle
import multiprocessing
from python_structured import python_query_parse, python_code_parse, python_context_parse
from sqlang_structured import sqlang_query_parse, sqlang_code_parse, sqlang_context_parse

def multipro_python_query(data_list):
    """并行解析Python查询数据。"""
    return [python_query_parse(line) for line in data_list]

def multipro_python_code(data_list):
    """并行解析Python代码数据。"""
    return [python_code_parse(line) for line in data_list]

def multipro_python_context(data_list):
    """并行解析Python上下文数据，处理特殊情况'-10000'。"""
    result = []
    for line in data_list:
        if line == '-10000':
            result.append(['-10000'])
        else:
            result.append(python_context_parse(line))
    return result

def multipro_sqlang_query(data_list):
    """并行解析SQL查询数据。"""
    return [sqlang_query_parse(line) for line in data_list]

def multipro_sqlang_code(data_list):
    """并行解析SQL代码数据。"""
    return [sqlang_code_parse(line) for line in data_list]

def multipro_sqlang_context(data_list):
    """并行解析SQL上下文数据，处理特殊情况'-10000'。"""
    result = []
    for line in data_list:
        if line == '-10000':
            result.append(['-10000'])
        else:
            result.append(sqlang_context_parse(line))
    return result

def parse(data_list, split_num, context_func, query_func, code_func):
    """
    使用提供的函数并行解析数据。

    参数:
        data_list (list): 需要解析的数据列表。
        split_num (int): 并行处理时每块的数据量。
        context_func (function): 解析上下文数据的函数。
        query_func (function): 解析查询数据的函数。
        code_func (function): 解析代码数据的函数。

    返回:
        tuple: 解析后的上下文、查询和代码数据。
    """
    pool = multiprocessing.Pool()
    split_list = [data_list[i:i + split_num] for i in range(0, len(data_list), split_num)]

    # 解析上下文数据
    context_data = [item for sublist in pool.map(context_func, split_list) for item in sublist]
    print(f'context条数：{len(context_data)}')

    # 解析查询数据
    query_data = [item for sublist in pool.map(query_func, split_list) for item in sublist]
    print(f'query条数：{len(query_data)}')

    # 解析代码数据
    code_data = [item for sublist in pool.map(code_func, split_list) for item in sublist]
    print(f'code条数：{len(code_data)}')

    pool.close()
    pool.join()

    return context_data, query_data, code_data

def main(lang_type, split_num, source_path, save_path, context_func, query_func, code_func):
    """
    主函数，用于解析语料并保存结果。

    参数:
        lang_type (str): 语言类型，如 'python' 或 'sql'。
        split_num (int): 并行处理时每块的数据量。
        source_path (str): 源数据文件路径。
        save_path (str): 保存解析后数据文件的路径。
        context_func (function): 解析上下文数据的函数。
        query_func (function): 解析查询数据的函数。
        code_func (function): 解析代码数据的函数。
    """
    # 读取源数据文件
    with open(source_path, 'rb') as f:
        corpus_list = pickle.load(f)

    # 并行解析数据
    context_data, query_data, code_data = parse(corpus_list, split_num, context_func, query_func, code_func)
    qids = [item[0] for item in corpus_list]

    # 汇总解析结果
    total_data = [[qids[i], context_data[i], code_data[i], query_data[i]] for i in range(len(qids))]

    # 保存解析后的数据
    with open(save_path, 'wb') as f:
        pickle.dump(total_data, f)

if __name__ == '__main__':
    split_num = 1000  # 定义每块并行处理的数据量，可以根据需要修改

    # Python数据路径
    staqc_python_path = './ulabel_data/python_staqc_qid2index_blocks_unlabeled.txt'
    staqc_python_save = '../hnn_process/ulabel_data/staqc/python_staqc_unlabled_data.pkl'
    large_python_path = './ulabel_data/large_corpus/multiple/python_large_multiple.pickle'
    large_python_save = '../hnn_process/ulabel_data/large_corpus/multiple/python_large_multiple_unlable.pkl'

    # SQL数据路径
    staqc_sql_path = './ulabel_data/sql_staqc_qid2index_blocks_unlabeled.txt'
    staqc_sql_save = './ulabel_data/staqc/sql_staqc_unlabled_data.pkl'
    large_sql_path = './ulabel_data/large_corpus/multiple/sql_large_multiple.pickle'
    large_sql_save = './ulabel_data/large_corpus/multiple/sql_large_multiple_unlable.pkl'

    # 处理Python数据
    main('python', split_num, staqc_python_path, staqc_python_save, multipro_python_context, multipro_python_query, multipro_python_code)
    main('python', split_num, large_python_path, large_python_save, multipro_python_context, multipro_python_query, multipro_python_code)

    # 处理SQL数据
    main('sql', split_num, staqc_sql_path, staqc_sql_save, multipro_sqlang_context, multipro_sqlang_query, multipro_sqlang_code)
    main('sql', split_num, large_sql_path, large_sql_save, multipro_sqlang_context, multipro_sqlang_query, multipro_sqlang_code)

    print('数据处理完成')
