# 完美编程-各个文件的说明

## 1.embddings_process.py
## 改进点
1. **代码规范化**：对原始代码进行了格式化，遵循了PEP 8规范，增加了注释和文档字符串，以提高代码的可读性和维护性。
2. **函数封装**：将功能相近的代码封装成函数，减少代码重复，提高代码的模块化程度。
3. **异常处理**：增加了对可能出现异常情况的处理，确保代码的健壮性。
4. **变量命名**：使用更具描述性的变量名，使代码更容易理解。
5. **冗余删除**：删除了不必要的代码，简化了代码结构。
6. **注释增加**：增加了详细的注释，解释每个函数的功能和参数，使读者更容易理解代码的逻辑。

## 代码总体结构

代码分为四个主要部分：
1. **词向量文件处理**：包括将词向量文件保存为二进制文件和构建新的词典及词向量矩阵。
2. **词典处理**：包括获取词在词典中的位置。
3. **语料序列化**：包括将训练、测试、验证语料进行序列化。
4. **主函数**：执行词典和词向量矩阵的构建以及语料的序列化。

## 函数说明
-  `save_word_vectors_as_binary(input_path, output_path)`：将词向量文件从文本格式转换为二进制格式，以加快后续加载速度。
- `build_new_dictionary_and_vectors(input_vec_path, input_word_path, output_vec_path, output_word_path)`：从输入的词向量文件和词典文件中构建新的词典和词向量矩阵，并将其保存为二进制文件。
- `get_word_index(type, text, word_dict)`：根据文本类型（`code` 或 `text`）获取词在词典中的位置列表。
- `serialize_corpus(word_dict_path, input_corpus_path, output_corpus_path)`：将输入的语料文件序列化并保存为二进制文件。

## 主函数
1. 加载词向量文件，并将其转换为二进制格式。
2. 构建新的词典和词向量矩阵，并将其保存为二进制文件。
3. 序列化语料文件，并将结果保存为二进制文件。

## 2.getStru2Vec.py

### 改进点

1. **代码规范化**：对原始代码进行了格式化，遵循PEP 8规范，增加了注释和文档字符串，以提高代码的可读性和维护性。
2. **函数封装**：将功能相近的代码封装成函数，减少代码重复，提高代码的模块化程度。
3. **变量命名**：使用更具描述性的变量名，使代码更容易理解。
4. **增加注释**：增加了详细的中文注释，解释每个函数的功能和参数，使读者更容易理解代码的逻辑。

### 代码总体结构

代码分为以下几个部分：
1. **并行数据解析函数**：包括并行解析Python和SQL的查询、代码和上下文数据的函数。
2. **数据解析主函数**：包括解析数据并调用并行解析函数的`parse`函数和主函数`main`。
3. **主入口**：包括读取数据源路径，调用主函数处理Python和SQL数据，并保存结果。

### 函数说明

-  `multipro_python_query(data_list)`:并行解析Python查询数据。
-  `multipro_python_code(data_list)`:并行解析Python代码数据。
- `multipro_python_context(data_list)`:并行解析Python上下文数据，处理特殊情况 `'-10000'`。
-  `multipro_sqlang_query(data_list)`：并行解析SQL查询数据。
-  `multipro_sqlang_code(data_list)`：并行解析SQL代码数据。
-  `multipro_sqlang_context(data_list)`：并行解析SQL上下文数据，处理特殊情况 `'-10000'`。
-  `parse(data_list, split_num, context_func, query_func, code_func)`：使用提供的函数并行解析数据。
- `main(lang_type, split_num, source_path, save_path, context_func, query_func, code_func)`：主函数，用于解析语料并保存结果。

## 3.process_single_corpus.py

## 改进点

1. **代码规范化**： 例如，在 `load_pickle` 函数中，增加了文档字符串和参数说明：
2. **函数封装**：例如，将处理staqc数据的代码封装成 `process_staqc_data` 函数：
3. **异常处理**：在 `load_pickle` 函数中增加了异常处理：
4. **变量命名**： 例如，将 `total_data_single` 和 `total_data_multiple` 改为 `single_data` 和 `multiple_data`：
5. **注释增加**：增加了详细的注释，解释每个函数的功能和参数，使读者更容易理解代码的逻辑。例如，在 `split_data` 函数中增加了详细的注释
    

## 代码总体结构

代码分为四个主要部分：

1. **数据加载**：包括从文件中加载pickle数据。
2. **数据拆分**：根据qids将数据分为单一和多重两部分。
3. **数据处理**：处理staqc和large数据，将其分为单一和多重两部分并保存。
4. **数据转换**：将单一未标记数据转换为标记数据。

## 函数说明
- `load_pickle(filename)`:从文件中加载pickle数据。
-  `split_data(total_data, qids)`:根据qids将数据分为单一和多重两部分。
- `process_staqc_data(filepath, single_save_path, multiple_save_path)`:处理staqc数据，将其分为单一和多重两部分并保存。
-  `process_large_data(filepath, single_save_path, multiple_save_path)`:处理large数据，将其分为单一和多重两部分并保存。
-  `convert_single_unlabeled_to_labeled(input_path, output_path)`:将单一未标记数据转换为标记数据。

## 主函数
1. 加载数据文件，并将其拆分为单一和多重两部分。
2. 处理staqc和large数据，将其分为单一和多重两部分并保存。
3. 将单一未标记数据转换为标记数据，并保存结果。

## 4.python_structured.py
## 改进点

1. **代码规范化**：例如在 python_parser 函数中，添加了详细的注释和文档字符串：
2. **函数封装**：将处理自然语言行的功能封装在 process_nl_line 函数中。
3. **冗余删除**：在 repair_program_io 函数中，简化了修复程序输入输出格式的逻辑。


## 代码总体结构

代码分为以下部分：

1. **修复程序输入输出格式**：包括修复程序输入输出格式的函数。
2. **Python代码解析**：包括解析Python代码、查询和上下文的函数。
3. **自然语言处理**：包括处理自然语言行、句子的函数。

## 函数说明

-  `repair_program_io(code)`:修复程序输入输出格式。
- `python_parser(code)`:解析Python代码，获取token列表和变量信息。
- `get_vars_heuristics(code)`:使用启发式方法获取代码中的变量名。
-  `python_code_parse(line)`:解析Python代码，获取token列表。
-  `python_query_parse(line)`:解析Python查询，获取token列表。
- `python_context_parse(line)`:解析Python上下文，获取token列表。
-  `process_nl_line(line)`:处理自然语言行，去除冗余信息。
-  `process_sent_word(line)`:处理句子，进行分词和词性还原。
-  `filter_all_invachar(line)`:去除所有非常用符号。
-  `filter_part_invachar(line)`:去除部分非常用符号。
-  `revert_abbrev(line)`:还原缩写词。
- `get_wordpos(tag)`:获取词性。

## 主函数
1. 解析Python查询和上下文，获取token列表。
2. 处理自然语言行，去除冗余信息。
3. 处理句子，进行分词和词性还原。

## 5.sqlang_structured.py

## 改进点

1. **代码规范化**：将正则表达式模式和替换字符串定义在 patterns 列表中，避免重复代码，提高可维护性。
2. **注释增加**：在每个子函数和主函数中添加了详细的注释，解释函数的功能和参数，使代码更易于理解。

## 代码总体结构

代码分为以下部分：

1. **正则表达式模式和替换字符串定义**：在 `patterns` 列表中定义了正则表达式模式和对应的替换字符串，用于处理缩写和词性标注。
2. **句子处理子函数**：包括处理自然语言行、分词和词性还原的子函数，用于对句子进行预处理和分析。
3. **代码解析主函数**：包括对代码的规则处理和解析的主函数，用于处理 SQL 代码的规则、分词和重命名标识符。

## 函数说明

-  `revert_abbrev(line)`：还原缩写词，根据预定义的正则表达式模式将缩写还原为完整词语。
-  `get_wordpos(tag)`：根据词性标记获取词性，返回对应的 WordNet 词性。
- `process_nl_line(line)`：处理自然语言行，去除冗余信息，将句子转换为下划线命名格式。
-  `process_sent_word(line)`：处理句子，进行分词和词性还原，返回分词后的单词列表。
-  `filter_all_invachar(line)`：去除所有非常用符号，保留常用符号和字符。
- `filter_part_invachar(line)`：去除部分非常用符号
- `sqlang_code_parse(line)`：解析 SQL 代码，获取 token 列表，包括处理正则表达式、分词和词性还原的逻辑。
- `sqlang_query_parse(line)`：解析 SQL 查询，获取 token 列表，包括处理非常用符号、自然语言行处理和分词的逻辑。
- `sqlang_context_parse(line)`：解析 SQL 上下文，获取 token 列表，包括处理部分非常用符号、自然语言行处理和分词的逻辑。

## 6.word_dict.py


## 改进点：
1. **函数命名规范化**：采用动词+名词的方式，清晰表达函数作用。原函数名 get_vocab 改为 build_vocabulary，更清晰地表达函数的作用。
2. **注释添加**：在函数内部添加了注释，说明函数的参数和返回值，提高了代码的可读性和可维护性。

## 代码总体结构：

1.**处理词汇文件** 定义构建词汇表、加载 pickle 数据和处理词汇文件的函数。
2.**设置路径主函数** ，设置各数据文件路径，并调用处理函数生成新的词汇文件。

## 函数说明：
-  `build_vocabulary(corpus1, corpus2)`: 从两个语料库构建词汇表。
-  `load_pickle_data(filename)`: 从 pickle 文件加载数据。
-  `process_vocabulary_files(file1, file2, save_path)`: 处理词汇文件，生成新的词汇文件。

