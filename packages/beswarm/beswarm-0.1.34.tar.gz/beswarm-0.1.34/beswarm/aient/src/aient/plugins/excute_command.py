import subprocess
from .registry import register_tool

import html

def unescape_html(input_string: str) -> str:
  """
  将字符串中的 HTML 实体（例如 &amp;）转换回其原始字符（例如 &）。

  Args:
    input_string: 包含 HTML 实体的输入字符串。

  Returns:
    转换后的字符串。
  """
  return html.unescape(input_string)

# 执行命令
@register_tool()
def excute_command(command):
    """
执行命令并返回输出结果
禁止用于查看pdf，禁止使用 pdftotext 命令

参数:
    command: 要执行的命令，可以克隆仓库，安装依赖，运行代码等

返回:
    命令执行的输出结果或错误信息
    """
    try:
        # 使用subprocess.run捕获命令输出
        command = unescape_html(command)
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        # 返回命令的标准输出
        if "pip install" in command:
            stdout_log = "\n".join([x for x in result.stdout.split('\n') if '━━' not in x])
        else:
            stdout_log = result.stdout
        return f"执行命令成功:\n{stdout_log}"
    except subprocess.CalledProcessError as e:
        if "pip install" in command:
            stdout_log = "\n".join([x for x in e.stdout.split('\n') if '━━' not in x])
        else:
            stdout_log = e.stdout
        # 如果命令执行失败，返回错误信息和错误输出
        return f"执行命令失败 (退出码 {e.returncode}):\n错误: {e.stderr}\n输出: {stdout_log}"
    except Exception as e:
        return f"执行命令时发生异常: {e}"

if __name__ == "__main__":
    print(excute_command("ls -l && echo 'Hello, World!'"))
    print(excute_command("ls -l &amp;&amp; echo 'Hello, World!'"))
