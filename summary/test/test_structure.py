from tree_utils.struct_tree_out import print_tree

path = r'../../summary'
exclude_dirs_set = {'test', 'okr.md', 'readme.md', '__init__.py'}
print_tree(directory=path, exclude_dirs=exclude_dirs_set)
