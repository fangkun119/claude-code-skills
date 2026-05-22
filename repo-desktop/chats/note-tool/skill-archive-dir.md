# 创建Skill

创建一个claude skill，用于archive一个目录。
传入给它要归档的文件路径, 例如"./to_path/target_dir/"，它会执行如下操作：
1. 首先会检查 ./to_path/target_dir.tar.gz 是否存在
2. 如果不存在，就用 ./to_path/target_dir/ 这个目录创建 ./to_path/target_dir.tar.gz
3. 如果存在，就把 ./to_path/target_dir/ 下所有文件添加到 ./to_path/target_dir.tar.gz ，如果要添加的文件在 tar.gz 文件中已经存在，就覆盖掉原来的文件（注意，它只会添加或覆盖文件，不会删除文件）
4. 它只依赖Python 3和UV，如果用户没有安装，会直接退出并提示用户
5. 它使用.venv虚拟环境中的Python来运行：如果用户的工作目录已有.venv，会直接使用；如果没有，会基于Python 3.12创建一个。
