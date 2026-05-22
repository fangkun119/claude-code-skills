AutoDL 使⽤

⽹址(cid:49482) http://autodl.com

按需使⽤

留意显存够不够⽤

选择基础镜像

使⽤提出的登录指令和密码就能登陆服务器了

因为是国内的机器(cid:49480) 访问 git 和 hugging face 会⾮常慢
可以使⽤学术资源加速

接下来搭建⼀个 ChatGLM3 (cid:49462)备注(cid:49482) ⽬前主要在⽤的已经是 ChatGLM4 了(cid:49473)
先 git clone

修改⼀下 requirements.txt (调试的时候总是有⼀个包冲突(cid:49480) 去掉发⽣冲突的那个包
的版本(cid:49480) 让 pip install 时⾃动选择版本(cid:49473)

⽤ chatglm3 给的 demo code 测试⼀下


