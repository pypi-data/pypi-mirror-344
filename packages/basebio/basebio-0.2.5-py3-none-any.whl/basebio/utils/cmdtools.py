# -*- coding: utf-8 -*-
__author__ = "legendzdy@dingtalk.com"
"""
Author: legendzdy@dingtalk.com
Data: 20250114
Description:
function map.
"""
import subprocess

def run_command(command: str|list, use_shell: bool=False) -> None:
    """
    执行任意shell命令的通用函数
    
    Args:
        command (str/list): 要执行的命令，可以是字符串格式或列表格式
        use_shell (bool): 是否使用shell模式执行（处理管道/重定向时需要设为True）
    
    Examples:
        #### 列表形式（推荐不需要shell特性时使用）
        run_command(['ls', '-l', '/tmp'])
        
        #### 字符串形式（需要处理管道时）
        run_command('ls -l /tmp | grep log', use_shell=True)
    """
    try:
        if isinstance(command, list):
            printable_command = ' '.join(command)
        else:
            printable_command = command
            
        print(f"Running command: {printable_command}")
        subprocess.run(
            command,
            check=True,
            shell=use_shell,
            # stderr=subprocess.PIPE,
            # stdout=subprocess.PIPE,
            # universal_newlines=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print(f"Error output: {e.stderr}")
        exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        exit(1)