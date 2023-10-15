
def read_variables_from_env(file_path='./.env'):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    variables = {}
    for line in lines:
        key, value = line.strip().split('=')
        variables[key] = value

    return variables