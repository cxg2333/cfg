# ### 找出每个结构无需迭代的数据数量
# import re

# def remove_bracketed_content(s):
#     return re.sub(r'\[.*?\]', '', s)

# structures = ["⿳", "⿱", "⿹", "⿰", "⿵", "⿻", "⿺", "⿴", "⿶", "⿸", "⿷", "⿲"]
# structure_count = {structure: 0 for structure in structures}
# without_structure_count = 0

# with open('filtered_ids.txt', 'r', encoding='utf-8') as file:
#     lines = file.readlines()
#     for line in lines:
#         parts = line.strip().split('\t')
#         if len(parts) >= 3:
#             unicode_code = parts[0]
#             character = parts[1]
#             structure = parts[2]
#             structure = remove_bracketed_content(structure)
            
#             if structure[0] in structures:
#                 if structure[0] in ["⿳", "⿲"] and len(structure)==4:
#                     structure_count[structure[0]] += 1
#                 elif structure[0] in ["⿱", "⿹", "⿰", "⿵", "⿻", "⿺", "⿴", "⿶", "⿸", "⿷"] and len(structure)==3:
#                     structure_count[structure[0]] += 1
#             else:
#                 without_structure_count += 1

# for structure, count in structure_count.items():
#     print(f"{structure} 的数量: {count}")

# print(f"isolate结构的字符数量: {without_structure_count}")


### 找出每个结构无需迭代的数据数量
import re

def remove_bracketed_content(s):
    return re.sub(r'\[.*?\]', '', s)
stru_info = "⿰"
stru_len = 3
lr_filtered_lines = []
with open('filtered_ids.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        parts = line.strip().split('\t')
        if len(parts) >= 3:
            unicode_code = parts[0]
            character = parts[1]
            structure = parts[2]
            structure = remove_bracketed_content(structure)
            if structure[0] == stru_info and len(structure)==stru_len:
                lr_filtered_lines.append(character+structure.replace(stru_info, '')+'\n')

with open('lr_filtered_ids.txt', 'w', encoding='utf-8') as output_file:
    output_file.writelines(lr_filtered_lines)
print("已成功写入")

                    

