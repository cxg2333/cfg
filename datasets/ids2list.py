### 从ids文件中提取出第二列，即所有字符
input_file_path = 'filtered_ids.txt'
output_file_path = 'char_list.txt' 

with open(input_file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

middle_column_chars = []

for line in lines:
    parts = line.strip().split('\t')
    if len(parts) >= 3: 
        middle_column_chars.append(parts[1])

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for char in middle_column_chars:
        output_file.write(char)

print(f"中间一列的字符已保存到 {output_file_path} 文件中。")
