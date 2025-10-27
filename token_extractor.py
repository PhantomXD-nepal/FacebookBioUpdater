import re
import json
from urllib.parse import unquote, parse_qs

def extract_tokens_from_fetch(fetch_code):
    tokens = {}
    
    try:
        headers_match = re.search(r'"headers":\s*{([^}]+)}', fetch_code, re.DOTALL)
        if headers_match:
            headers_text = headers_match.group(1)
            
            lsd_match = re.search(r'"x-fb-lsd":\s*"([^"]+)"', headers_text)
            if lsd_match:
                tokens['x_fb_lsd'] = lsd_match.group(1)
            
            cookie_match = re.search(r'"cookie":\s*"([^"]+)"', headers_text)
            if cookie_match:
                tokens['cookie'] = cookie_match.group(1)
                
                cookie_str = cookie_match.group(1)
                
                c_user_match = re.search(r'c_user=(\d+)', cookie_str)
                if c_user_match:
                    tokens['user_id'] = c_user_match.group(1)
                
                tokens['cookie_parts'] = {}
                cookie_parts = ['datr', 'sb', 'fr', 'xs', 'c_user', 'dpr']
                for part in cookie_parts:
                    part_match = re.search(f'{part}=([^;]+)', cookie_str)
                    if part_match:
                        tokens['cookie_parts'][part] = part_match.group(1)
        
        body_match = re.search(r'"body":\s*"([^"]+)"', fetch_code)
        if body_match:
            body_text = unquote(body_match.group(1))
            
            body_params = {}
            for param in body_text.split('&'):
                if '=' in param:
                    key, value = param.split('=', 1)
                    body_params[key] = unquote(value)
            
            important_params = [
                'fb_dtsg', 'jazoest', 'lsd', '__rev', '__spin_r',
                '__spin_b', '__spin_t', 'av', '__user', 'doc_id'
            ]
            
            for param in important_params:
                if param in body_params:
                    tokens[param] = body_params[param]
            
            if 'variables' in body_params:
                try:
                    tokens['variables'] = json.loads(body_params['variables'])
                except:
                    tokens['variables'] = body_params['variables']
        
        referrer_match = re.search(r'"referrer":\s*"([^"]+)"', fetch_code)
        if not referrer_match:
            referrer_match = re.search(r'"Referer":\s*"([^"]+)"', fetch_code)
        if referrer_match:
            tokens['referer'] = referrer_match.group(1)
        
        url_match = re.search(r'fetch\("([^"]+)"', fetch_code)
        if url_match:
            tokens['url'] = url_match.group(1)
        
        friendly_name_match = re.search(r'"x-fb-friendly-name":\s*"([^"]+)"', fetch_code)
        if friendly_name_match:
            tokens['api_endpoint'] = friendly_name_match.group(1)
        
    except Exception as e:
        print(f"Error during extraction: {e}")
    
    return tokens


def save_tokens_to_file(tokens, filename="extracted_tokens.json"):
    with open(filename, 'w') as f:
        json.dump(tokens, f, indent=2)


def generate_python_config(tokens):
    config = f'''USER_ID = "{tokens.get('user_id', '')}"
API_ENDPOINT = "{tokens.get('api_endpoint', '')}"
REFERER = "{tokens.get('referer', '')}"
FB_DTSG = "{tokens.get('fb_dtsg', '')}"
X_FB_LSD = "{tokens.get('x_fb_lsd', '')}"
LSD = "{tokens.get('lsd', '')}"
JAZOEST = "{tokens.get('jazoest', '')}"
COOKIE = "{tokens.get('cookie', '')}"
DOC_ID = "{tokens.get('doc_id', '')}"
__REV = "{tokens.get('__rev', '')}"
__SPIN_R = "{tokens.get('__spin_r', '')}"
__SPIN_B = "{tokens.get('__spin_b', '')}"
__SPIN_T = "{tokens.get('__spin_t', '')}"
URL = "{tokens.get('url', 'https://www.facebook.com/api/graphql/')}"
'''
    return config


if __name__ == "__main__":
    file_path = input("Enter the path to the fetch request file: ")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            fetch_code = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        exit(1)
    
    tokens = extract_tokens_from_fetch(fetch_code)
    
    if not tokens:
        print("Failed to extract tokens")
        exit(1)
    
    save_tokens_to_file(tokens)
    
    config_code = generate_python_config(tokens)
    
    with open("tokens.py", 'w') as f:
        f.write(config_code)
    
    print("Done")