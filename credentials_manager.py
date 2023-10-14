
def read_credentials_from_env(file_path='./.env'):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    credentials = {}
    for line in lines:
        key, value = line.strip().split('=')
        credentials[key] = value

    return credentials['username'], credentials['password']