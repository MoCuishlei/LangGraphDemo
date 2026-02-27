import os
from git import Repo
from src.config import REPOS_DIR

def clone_or_update_repo(git_url: str) -> str:
    """
    克隆 Git 仓库或拉取最新更新。
    返回本地仓库路径。
    """
    try:
        # 从 URL 中提取项目名作为文件夹名
        repo_name = git_url.split('/')[-1].replace('.git', '')
        local_path = os.path.join(REPOS_DIR, repo_name)

        if os.path.exists(local_path):
            print(f"Directory {local_path} exists. Using local version...")
            return local_path
        else:
            print(f"Cloning {git_url} to {local_path}...")
            Repo.clone_from(git_url, local_path)
        
        return local_path
    except Exception as e:
        print(f"Error handling Git repo {git_url}: {e}")
        return ""

if __name__ == "__main__":
    # 测试代码
    path = clone_or_update_repo("https://github.com/mock-repo/test.git")
    print(f"Local path: {path}")
