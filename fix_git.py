
#报错 fatal: bad source 是因为在 Windows 环境下，Git 无法在磁盘上找到这个带尖括号的原始文件，所以它不知道该“移动”谁。
import subprocess
import os

# 自动处理中文路径编码
os.environ["PYTHONIOENCODING"] = "utf-8"

def fix_filenames():
    # 1. 设置 Git 不要在输出中对中文文件名进行转义
    subprocess.run(["git", "config", "core.quotepath", "false"])

    print("--- 开始扫描非法文件名 ---")
    
    # 2. 从 Git 原始数据库中读取所有文件（包括 Windows 无法显示的文件）
    # ls-tree -r HEAD 会列出仓库里真实存在的所有文件信息
    cmd = ["git", "ls-tree", "-r", "HEAD"]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    
    found = False
    for line in result.stdout.splitlines():
        # line 格式: 100644 blob <hash> <filename>
        parts = line.split(maxsplit=3)
        if len(parts) < 4: continue
        
        mode, type_, blob_hash, old_path = parts
        
        # 检查是否包含 Windows 不允许的字符: < > : " / \ | ? *
        # 这里主要处理你遇到的 < >
        if "<" in old_path or ">" in old_path:
            found = True
            # 生成新文件名：把 < > 替换为中文括号，或者直接删掉
            new_path = old_path.replace("<", "（").replace(">", "）")
            
            print(f"发现非法文件: {old_path}")
            print(f"准备重命名为: {new_path}")
            
            try:
                # A. 【核心魔法】直接在索引中添加新条目，指向原始内容（blob_hash）
                # 这一步不需要物理文件存在，所以不会报错
                subprocess.run(["git", "update-index", "--add", "--cacheinfo", mode, blob_hash, new_path], check=True)
                
                # B. 从索引中强制移除旧的非法条目
                subprocess.run(["git", "rm", "--cached", "--force", old_path], stdout=subprocess.DEVNULL, check=True)
                
                print(">>> 修复成功！(索引已更新)")
                
            except subprocess.CalledProcessError as e:
                print(f"!!! 修复失败: {e}")

    if not found:
        print("未发现非法文件名。如果 VS Code 还在报错，请尝试重启 VS Code。")
    else:
        print("\n--- 处理完毕 ---")
        print("下一步：请在终端运行 'git commit -m \"Fix filenames\"' 提交修改。")

if __name__ == "__main__":
    fix_filenames()