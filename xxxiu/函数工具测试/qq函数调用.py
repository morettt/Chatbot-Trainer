import subprocess

def run_command():
    directory_path = r"C:\Program Files\Tencent\QQNT"
    batch_file = "QQ.exe"
    try:
        command = f"{batch_file}"
        subprocess.Popen(["cmd.exe", "/c", command], cwd=directory_path, creationflags=subprocess.CREATE_NO_WINDOW)
    except Exception as e:
        return f"打开QQ时出错：{str(e)}"

print(run_command())
