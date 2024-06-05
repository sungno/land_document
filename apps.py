from moduls import *
from method import *

from mdriver import *

# import sys
# import types


def download_script(url):
    headers = {'Cache-Control': 'no-cache'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def load_module_from_string(module_name, module_content):
    module = types.ModuleType(module_name)
    exec(module_content, module.__dict__)
    sys.modules[module_name] = module
    return module

def download_and_load_all_scripts(scripts_json_url):
    scripts_content = download_script(scripts_json_url)
    scripts_data = json.loads(scripts_content)
    for script_url in scripts_data["scripts"]:
        script_name = script_url.split('/')[-1].split('.')[0]
        print(script_name)
        script_content = download_script(script_url)
        load_module_from_string(script_name, script_content)

try:
    # scripts.json 파일의 URL
    scripts_json_url = "https://raw.githubusercontent.com/sungno/land_document/main/scripts.json"
    # 모든 스크립트 다운로드 및 로드
    download_and_load_all_scripts(scripts_json_url)



    ################### 실행 코드 시작 ###########################################
    print("성공")

except Exception as e:
    print(f"[apps.py] An error occurred: {e}")