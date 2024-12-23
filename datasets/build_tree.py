import json
import re

def remove_bracketed_content(s):
    # 使用正则表达式匹配并删除 [****] 及其中的内容
    return re.sub(r'\[.*?\]', '', s)

class TreeNode:
    def __init__(self, value):
        self.value = value  # 节点的值（结构或组件）
        self.children = []  # 子节点列表

    def add_child(self, child_node):
        self.children.append(child_node)

    def to_dict(self):
        return {
            "value": self.value,
            "children": [child.to_dict() for child in self.children]
        }

    def __repr__(self, level=0):
        ret = "\t" * level + repr(self.value) + "\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret

# 存储Unicode字符及其结构和组件信息
unicode_data = {}

# 从文件读取数据
with open('filtered_ids.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        parts = line.strip().split('\t')
        if len(parts) >= 3:
            unicode_code = parts[0]
            character = parts[1]
            structure = parts[2]
            structure = remove_bracketed_content(structure)

            # 解析结构字符串，构建树
            stack = []  # 使用栈来构建树
            current_node = None  # 当前节点初始化为 None

            for char in structure:
                if char in ["⿳", "⿱", "⿹", "⿰", "⿵", "⿻", "⿺", "⿴", "⿶", "⿸", "⿷", "⿲"]:  # 结构节点
                    new_node = TreeNode(char)
                    if current_node is None:
                        current_node = new_node
                    else:
                        current_node.add_child(new_node)
                    stack.append(current_node) 
                    current_node = new_node
                else:  
                    new_node = TreeNode(char)
                    if current_node is None:
                        current_node = new_node
                    else:
                        current_node.add_child(new_node)

                    while stack:
                        if current_node.value in ["⿳", "⿲"]:
                            if len(current_node.children) == 3:
                                current_node = stack.pop()
                            else:
                                break
                        else:
                            if len(current_node.children) == 2:
                                current_node = stack.pop()
                            else:
                                break

            unicode_data[unicode_code] = {
                "character": character,
                "structure": current_node.to_dict()
            }

# 打印结果
# for unicode_code, info in unicode_data.items():
#     print(f"{unicode_code}: {info['character']}")
#     print("结构树:")
#     print(info['structure'])

with open("char_tree.json", "w", encoding="utf-8") as f:
    json.dump(unicode_data,f,ensure_ascii=False, indent=4)
    print(f"字符树已经保存到char_tree中")