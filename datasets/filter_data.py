### 将找不到相应图片的字符删掉
### 同时将构件中能用到这些字符的数据删掉
### 删除了1537条数据

special_chars = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩', '⑪', '⑫', '⑬', '⑭', '⑮', '⑯', '⑲', 
                '⺀', '⺆', '⺊', '⺸', '⺼', '㇀', '㇇', '㇉', '㇋', '㇌', '㇍', '㇎', '㇓', '㇞', '㇢', '㇣', '𛂦',
                'ℓ', 'い', 'よ', 'り', 'コ', 'サ', 'ス', 'ユ']

filtered_lines = []
num = 0
# 从文件读取数据
with open('ids.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        parts = line.strip().split('\t')
        if len(parts) >= 3:
            unicode_code = parts[0]
            character = parts[1]
            structure = parts[2]
            contains_special_char = any(char in structure for char in special_chars)
            if character in special_chars:
                contains_special_char = True
            if contains_special_char:
                num+=1
            else:
                filtered_lines.append(line)

            # unicode_data[unicode_code] = {
            #     "character": character,
            #     "structure": current_node
            # }
with open('filtered_ids.txt', 'w', encoding='utf-8') as output_file:
    output_file.writelines(filtered_lines)

print(f"有{num}条数据不能用")

# with open("char_tree.json", "w", encoding="utf-8") as f:
#     json.dump(unicode_data,f,ensure_ascii=False, indent=4)
#     print(f"字符树已经保存到char_tree中")