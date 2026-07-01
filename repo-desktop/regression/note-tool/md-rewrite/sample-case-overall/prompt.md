```text
/note-tool:md-rewrite @"sample_file.md"

用户原始需求见 @user_input.md
requirements 文档见 @requirements.md 
注意提取图片文字描述时，控制对大模型的访问并发度，一张一张串行处理，避免触发rate limiter限制
```