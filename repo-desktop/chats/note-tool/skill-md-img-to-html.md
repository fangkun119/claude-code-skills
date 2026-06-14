/skill-creator  在 note-tool 这个 plugin 里面加一个 skill,  它可以把用户传入的文档中，所有 Markdown 格式的图片，都转换为 HTML 标签格式的图片。

Markdown格式的图片形如：![[图片路径]] 或者 ![替换文字](图片路径)
转换后的HTML标签格式形如：
<img src="图片文件路径" style="display: block; width: 100%;" alt="替换文字">

如果Markdown格式的图片制定了宽度，那么转换成HTML标签后同样要保留宽度
例如
![[图片路径|600px]] 或者 ![替换文字|600px](图片链接)
转换后的HTML标签格式变成
<img src="图片文件路径" style="display: block; width: 600px;" alt="替换文字">

如果Markdown格式的图片没有替换文字，则HTML标签的替换文字为""
如果Markdown格式的图片没有指定宽度，则HTML标签的宽度为100%

这个Skill应当先梳理文件中所有的markdown格式的图片、它们的替换文字、宽度，文件中的位置。然后列出计划，按照在文中出现的位置、从下到上逆序完成。

逆序的原因是：先修改下面的图片，不会改变上面图片的位置，确保列出的计划依旧可行

