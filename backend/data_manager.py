def load_knowledge_base(file_path: str) -> str:
    with open(file_path, 'r') as file:
        knowledge_base = file.read()
    return knowledge_base

def log_chat(file_path: str, log_entry: str) -> None:
    with open(file_path, 'a') as file:
        file.write(log_entry + '\n')