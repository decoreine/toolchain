def interpret_blocks(blocks):
    class_code = ""
    method_code = ""
    part_code = {}
    for block in blocks:
        block_type = block["type"]
        if block_type == "class":
            class_code = block["content"]
        elif block_type == "method":
            method_code = f"\n\npublic function {block['name']}({block['parameters'][0]['name']}) {{\n"
            method_code += f"    {block['content']}\n}}"
        elif block_type == "part":
            part_code["content"] = block["content"]
            part_code["method"] = block["method"]
    return class_code, method_code, part_code