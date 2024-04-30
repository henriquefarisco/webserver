import os

def list_files(startpath):
    tree = []
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        tree.append(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            tree.append(f"{subindent}{f}")
    return '\n'.join(tree)

def main():
    startpath = '.'  # Define o diretório raiz como o diretório atual
    structure = list_files(startpath)
    with open('structure.txt', 'w') as f:
        f.write(structure)

if __name__ == "__main__":
    main()
