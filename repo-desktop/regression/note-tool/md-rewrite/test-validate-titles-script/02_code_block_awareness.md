## 1. 代码块感知功能测试

这是测试代码块感知功能的文档。

```python
# 这是Python代码块内的注释，不应该被识别为标题
## 代码块内的双井号
### 代码块内的三井号
def test_function():
    # 函数内的注释
    ## 代码块注释
    return "test"
```

### 1.1 代码块后的正常标题

这是代码块结束后应该被正确识别的标题。

#### (1) JavaScript代码块测试

```javascript
// JavaScript代码块
## JS代码块内的井号
### 更多JS注释
function jsTest() {
    return true;
}
```

##### ① Java代码块

```java
// Java代码块
public class JavaTest {
    // Java注释
}
```

## 2. 嵌套代码块测试

````四个反引号围栏开始
# 这些是代码内容，不应被识别为标题
## 继续代码块内容
### 更多代码块注释
````三个反引号不会关闭四个反引号的围栏
#### 仍然在代码块内
````
                                         ← 只包含4个反引号，关闭代码块

### 2.1 围栏后的标题

这是嵌套代码块后应该被识别的正常标题。

```python
# 另一个代码块
## 代码块内容
def another_test():
    pass
```

#### (2) 缩进代码块测试

   ```python
   # 带有3个空格缩进的代码块
   ## 应该被识别为代码块，不是标题
   def indented_function():
       return "indented"
   ```

##### ② 正常的四级标题

这是缩进代码块后应该被正确识别的四级标题。

## 3. 多语言代码块

### 3.1 不同编程语言

#### (1) YAML配置

```yaml
# YAML配置文件
spring:
  application:
    name: demo-service
## 配置注释
### 更多配置
```

##### ③ Shell脚本

```bash
#!/bin/bash
# Shell脚本注释
## 更多shell注释
echo "test"
```