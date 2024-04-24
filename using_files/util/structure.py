# pip install easy-media-utils
from tree_utils.struct_tree_out import print_tree

path = r'../../../LLM-EASY-WEBUI'
exclude_dirs_set = {'using_files', 'siscon_no_chroma_db', '.gitignore', 'LICENSE', 'requirements.txt', 'README.md'}
print_tree(directory=path, exclude_dirs=exclude_dirs_set)
