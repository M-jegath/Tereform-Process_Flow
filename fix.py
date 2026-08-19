import os
import glob

files = glob.glob('**/*.py', recursive=True)
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace backslash escaped quotes with just quotes
    new_content = content.replace('\\"\\"\\"', '"""')
    new_content = new_content.replace('\\\n', '\n')
    
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"Fixed {f}")
