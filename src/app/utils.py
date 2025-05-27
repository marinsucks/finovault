import os

def build_tree(path):
	tree = {}
	dirs = []
	files = []
	for entry in os.listdir(path):
		full_path = os.path.join(path, entry)
		if os.path.isdir(full_path):
			dirs.append(entry)
		else:
			files.append(entry)
	for entry in sorted(dirs):
		full_path = os.path.join(path, entry)
		tree[entry] = build_tree(full_path)
	if files:
		tree['__files__'] = sorted(files)
	return tree
