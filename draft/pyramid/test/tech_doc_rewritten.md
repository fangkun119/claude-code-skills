---
title: Elasticsearch参考3：提升搜索相关性
author: fangkun119
date: 2025-06-01 17:29:00 +0800
categories: [中间件, Elasticsearch]
tags: [Elasticsearch]
pin: false
math: true
mermaid: true
image:
  path: /imgs/cover/elasticsearch.svg
  lqip: data:image/webp;base64,UklGRpoAAABXRUJQVlA4WAoAAAAQAAAADwAABwAAQUxQSDIAAAARL0AmbZurmr57yyIiqE8oiG0bejIYEQTgqiDA9vqnsUSI6H+oAERp2HZ65qP/VIAWAFZQOCBCAAAA8AEAnQEqEAAIAAVAfCWkAALp8sF8rgRgAP7o9FDvMCkMde9PK7euH5M1m6VWoDXf2FkP3BqV0ZYbO6NA/VFIAAAA
  alt: Responsive rendering of Chirpy theme on multiple devices.
---

{: .no_toc }

<details close markdown="block">
  <summary>
    目录
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

# Elasticsearch搜索相关性优化完全指南

## 1. 相关性评分基础与概述

### 1.1 搜索相关性的核心定义

**用户对搜索结果的期望主要集中在四个关键方面**：

* **信息完整性**：能够找到所有相关的内容，不遗漏重要信息
* **结果准确性**：返回的结果中不相关的内容越少越好
* **评分合理性**：文档的相关性评分应该准确反映其匹配程度
* **业务适配性**：排序结果要符合具体的业务需求和用户偏好

**Elasticsearch使用相关性分数(_score)来量化文档与查询的匹配程度**，评分越高说明相关性越强，用户越容易找到想要的内容。

**以"JAVA多线程设计模式"这个查询为例**，查询词会被分词成三个关键词，每个关键词都能匹配到不同的文档。下表清楚地显示了文档2和文档3的相关性更高：

| 关键词   | 文档ID      |
| :------- | :---------- |
| JAVA     | 1,2,3       |
| 设计模式 | 1,2,3,4,5,6 |
| 多线程   | 2,3,7,9     |

**虽然Elasticsearch提供了默认的相关性计算方法**，但它也允许用户根据特定的业务需求来自定义相关性计算，让搜索结果更符合实际使用场景。

### 1.2 Elasticsearch相关性评分机制

#### 1.2.1 实用评分函数的工作原理

**Elasticsearch采用了一种两阶段的评分方法**：

* **第一阶段**：使用布尔模型快速筛选出匹配的文档
* **第二阶段**：通过"实用评分函数"精确计算每个文档的相关性分数

**这个评分公式融合了多种先进技术**：

* **理论基础**：借鉴了经典的TF-IDF（词频-逆向文档频率）和向量空间模型
* **现代优化**：加入了协调因子、字段长度归一化、词权重提升等新特性
* **算法演进**：Elasticsearch 5之前使用TF-IDF，5之后升级到更先进的Okapi BM25算法

**BM25算法的名称含义很有意思**：
* **BM**：代表"Best Match"（最佳匹配）
* **25**：表示经过25次迭代优化得出的最终版本
* **算法优势**：相比TF-IDF，BM25在保持准确性的同时增加了更多可调参数

#### 1.2.2 TF-IDF与BM25算法对比

**这两种算法都基于相同的核心假设**：

* **稀有词更重要**：使用逆向文档频率区分普通词汇（如"的"、"是"）和专业词汇
* **频率反映相关性**：词在文档中出现频率越高，相关性通常越强

**从逻辑角度看，这个假设非常直观**：
* **文档内频率**：某个词在当前文档中越频繁出现，说明这个文档越相关
* **跨文档频率**：某个词在所有文档中出现越频繁，说明它越通用，权重应该越低
* **综合效果**：越罕见的词在当前文档中频繁出现，越能代表这个文档的核心主题

**BM25相比TF-IDF有了显著的改进**：

* **参数灵活性**：增加了可调节的参数，使算法更加强大和实用
* **饱和机制**：TF-IDF中词频越高分数越高，而BM25的分数会趋于一个饱和值，避免了某个词过度影响评分

#### 1.2.3 TF-IDF核心组件详解

**TF-IDF算法由三个核心组件构成**，它们在索引时计算并存储，最终组合成单个词的权重：

**词频（TF - Term Frequency）**
* **基本原理**：检索词在文档中出现的次数越多，相关性越高
* **计算公式**：TF = 某个词在文档中的出现次数 ÷ 文档的总词数
* **实际效果**：确保包含更多搜索词的文档获得更高分数

**逆向文档频率（IDF - Inverse Document Frequency）**
* **核心理念**：在所有文档中越常见的词，重要性越低
* **计算逻辑**：IDF = log(语料库文档总数 ÷ (包含该词的文档数 + 1))
* **实际作用**：降低"的"、"是"、"在"等通用词的权重，提升专业词汇的重要性

**字段长度归一值（Field-length Norm）**
* **设计思想**：短字段中的匹配比长字段中的匹配更有意义
* **实际效果**：搜索词出现在标题字段比出现在正文字段获得更高权重
* **应用场景**：确保精确匹配不被长文档稀释

#### 1.2.4 使用Explain API查看TF-IDF评分详情

**Elasticsearch提供了Explain API来帮助理解评分机制**，下面是一个具体的示例：

```text
PUT /test_score/_bulk
{"index":{"_id":1}}
{"content":"we use Elasticsearch to power the search"}
{"index":{"_id":2}}
{"content":"we like elasticsearch"}
{"index":{"_id":3}}
{"content":"Thre scoring of documents is caculated by the scoring formula"}
{"index":{"_id":4}}
{"content":"you know,for search"}

GET /test_score/_search
{
  "explain": true,
  "query": {
    "match": {
      "content": "elasticsearch"
    }
  }
}

GET /test_score/_explain/2
{
  "query": {
    "match": {
      "content": "elasticsearch"
    }
  }
}
```

**通过Explain API，你可以清楚地看到**：
* 每个文档的详细评分过程
* 每个词对总分的贡献
* 各种评分因素的具体数值

### 1.3 自定义相关性评分的必要性与应用

#### 1.3.1 自定义评分的主要应用场景

**自定义相关性评分通过修改Elasticsearch的默认评分计算**，让最符合用户期望的结果排在前面，满足特定应用场景的需求。

**自定义评分在以下四个场景中特别有价值**：

* **个性化排序偏好**：根据用户习惯调整搜索结果的排序，让不同用户看到最适合自己的结果
* **业务字段权重优化**：给重要字段（如商品标题、价格）赋予更高权重，让业务关键因素影响排序
* **复杂业务逻辑集成**：将库存状态、促销活动等业务因素融入评分逻辑
* **用户行为数据融合**：利用点击率、购买转化率等用户行为数据优化搜索体验

#### 1.3.2 自定义评分的战略意义

**搜索引擎的本质是一个匹配过程**：从海量数据中精准找到满足用户需求的内容。

**相关性判断一直是搜索引擎领域的核心挑战**，因为：
* **用户意图复杂**：用户查询往往简短，但背后有复杂的真实需求
* **内容多样性强**：网页、文档、商品等不同类型内容需要不同的相关性标准
* **场景差异大**：学术搜索和商品搜索的相关性标准完全不同

**如果搜索引擎不能准确理解用户意图**，将相关结果排在前面，就会严重影响用户体验和满意度。这就是为什么自定义相关性评分如此重要的根本原因。

## 2. 自定义评分策略体系与实现方法

### 2.1 自定义评分策略的整体架构

**实现自定义评分策略可以从三个层面入手**：

* **索引层面**：在数据存储时就影响相关性计算
* **查询层面**：在执行搜索时动态调整评分
* **后处理层面**：对初步结果进行二次优化

**以下是五种主要的自定义评分策略**：

* **Index Boost**：在索引层面为不同索引设置不同权重
* **Boosting**：为不同查询条件设置不同的权重系数
* **Negative Boost**：对满足特定条件的结果进行降权处理
* **Function Score**：通过自定义函数实现复杂的评分逻辑
* **Rescore Query**：对查询结果进行二次评分和重新排序

### 2.2 Index Boost策略：跨索引权重分配

#### 2.2.1 应用场景与原理

**Index Boost策略特别适合跨索引搜索的场景**，比如搜索包含多种类型数据的系统。

**一个典型的实际应用是**：一批数据包含不同标签，数据结构相同，需要将不同标签存储在不同索引中，并按标签优先级展示结果（如A类优先，然后是B类，最后是C类）。

#### 2.2.2 具体实现示例

**下面通过一个完整的示例来演示Index Boost的实现**：

```text
PUT my_index_100a/_doc/1
{
  "subject": "subject 1"
}

PUT my_index_100b/_doc/1
{
  "subject": "subject 1"
}

PUT my_index_100c/_doc/1
{
  "subject": "subject 1"
}

POST my_index_100*/_search
{
  "query": {
    "term": {
      "subject.keyword": {
        "value": "subject 1"
      }
    }
  }
}

POST my_index_100*/_search
{
  "query": {
    "term": {
      "subject.keyword": {
        "value": "subject 1"
      }
    }
  },
  "indices_boost": [
    {
      "my_index_100a": 1.5
    },
    {
      "my_index_100b": 1.2
    },
    {
      "my_index_100b": 1.2
    }
  ]
}
```

**通过indices_boost参数，我们可以精确控制**：
* **my_index_100a**：权重提升1.5倍，最高优先级
* **my_index_100b**：权重提升1.2倍，中等优先级
* **my_index_100c**：默认权重，最低优先级

### 2.3 Boosting策略：查询条件权重优化

#### 2.3.1 工作机制与参数说明

**Boosting策略的核心思想是**：当有多个查询条件时，为不同条件设置不同的权重系数，影响最终的相关性评分。

**boosting参数的取值规则很直观**：

* **0-1之间的值**：表示降权处理（如0.2表示降低到原来的20%）
* **大于1的值**：表示提升权重（如1.5表示提升到原来的150%）

#### 2.3.2 实际应用示例

**下面的例子展示了如何为标题和内容字段设置不同权重**：

```text
POST /blogs/_bulk
{"index":{"_id":1}}
{"title":"Apple iPad","content":"Apple iPad,Apple iPad"}
{"index":{"_id":2}}
{"title":"Apple iPad,Apple iPad","content":"Apple iPad"}

GET /blogs/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "match": {
            "title": {
              "query": "apple,ipad",
              "boost": 4
            }
          }
        },
        {
          "match": {
            "content": {
              "query": "apple,ipad",
              "boost": 1
            }
          }
        }
      ]
    }
  }
}
```

**在这个查询中**：
* **标题匹配**：权重提升4倍，说明标题中的关键词更重要
* **内容匹配**：使用默认权重1倍
* **实际效果**：标题中包含"apple,ipad"的文档会获得更高分数

### 2.4 Negative Boost策略：选择性降权处理

#### 2.4.1 原理与使用场景

**Negative Boost提供了一种温和的过滤方式**：当某些结果不完全符合要求，但又不想完全排除它们时，可以通过降低权重来处理。

**Negative Boost的工作机制很巧妙**：

* **选择性应用**：只对查询中定义为negative的部分生效
* **权重调整**：给命中negative条件的文档乘以一个小于1的系数（如0.3）
* **保留可见性**：降权而不是排除，相关结果仍然可以出现，只是位置靠后

**一个经典的应用场景是**：苹果公司产品搜索。
* **问题**：用户搜索"apple"时，希望优先看到苹果公司产品，但不想完全排除"apple pie"等相关内容
* **Must Not方案**：使用must_not会完全过滤掉"apple pie"等不相关内容，可能过于严格
* **Negative Boost方案**：降低"apple pie"等内容的权重，让它们排在后面，但仍然可见

#### 2.4.2 实现对比示例

**下面的代码对比了三种不同的处理方式**：

```text
POST /news/_bulk
{"index":{"_id":1}}
{"content":"Apple Mac"}
{"index":{"_id":2}}
{"content":"Apple iPad"}
{"index":{"_id":3}}
{"content":"Apple employee like Apple Pie and Apple Juice"}

GET /news/_search
{
  "query": {
    "bool": {
      "must": {
        "match": {
          "content": "apple"
        }
      }
    }
  }
}

# 利用must not排除不是苹果公司产品的文档
GET /news/_search
{
  "query": {
    "bool": {
      "must": {
        "match": {
          "content": "apple"
        }
      },
      "must_not": {
        "match": {
          "content": "pie"
        }
      }
    }
  }
}

# 利用negative_boost降低相关性
GET /news/_search
{
  "query": {
    "boosting": {
      "positive": {
        "match": {
          "content": "apple"
        }
      },
      "negative": {
        "match": {
          "content": "pie"
        }
      },
      "negative_boost": 0.2
    }
  }
}
```

**三种方案的对比效果**：
* **普通搜索**：包含"apple pie"的文档也会正常显示
* **Must Not方案**：完全排除包含"pie"的文档，结果可能过于严格
* **Negative Boost方案**：降低包含"pie"文档的权重到20%，让苹果公司产品优先显示，但相关内容仍然可见

### 2.5 Function Score策略：自定义评分公式

#### 2.5.1 功能特点与应用场景

**Function Score是最强大的自定义评分策略**，它允许用户通过自定义查询语句和脚本，实现高度个性化的排序控制。

**Function Score特别适合复杂的业务场景**，比如：

* **电商商品排序**：结合相关性评分、销量、用户评价等多个因素
* **内容推荐**：考虑用户兴趣、内容热度、时效性等维度
* **地理位置搜索**：结合距离、评分、可用性等因素

**以商品搜索为例**：除了文字相关性，还希望根据销量和浏览人数来调整排序权重。

**考虑以下商品数据**：

| 商品 | 销量 | 浏览人数 |
| :--- | :--- | :------- |
| A    | 10   | 10       |
| B    | 20   | 20       |

**我们可以设计这样的评分公式**：
**最终评分 = 原始相关性评分 × (销量 + 浏览人数)**

**这个设计的优势在于**：
* **多维度考量**：不仅考虑文本匹配度，还融入了商业指标
* **业务导向**：销量和浏览人数高的商品获得更高排名
* **用户体验**：热销商品排在前面，提高用户购买转化率

#### 2.5.2 Script Score实现方式

**通过Script Score，我们可以实现上述的自定义评分逻辑**：

```text
PUT my_index_products/_bulk
{"index":{"_id":1}}
{"name":"A","sales":10,"visitors":10}
{"index":{"_id":2}}
{"name":"B","sales":20,"visitors":20}
{"index":{"_id":3}}
{"name":"C","sales":30,"visitors":30}

# 基于function_score实现自定义评分检索
POST my_index_products/_search
{
  "query": {
    "function_score": {
      "query": {
        "match_all": {}
      },
      "script_score": {
        "script": {
          "source": "_score*(doc['sales'].value+doc['visitors'].value)"
        }
      }
    }
  }
}
```

**这个查询的工作原理**：
* **基础查询**：`match_all`获取所有商品
* **评分脚本**：`_score*(doc['sales'].value+doc['visitors'].value)`
* **计算过程**：原始相关性分数 × (销量 + 浏览人数)
* **最终效果**：商品C (30+30=60) > 商品B (20+20=40) > 商品A (10+10=20)

### 2.6 Rescore Query策略：二次评分优化

#### 2.6.1 二次评分的工作原理

**Rescore Query提供了两阶段评分的机制**：先进行初步搜索，然后对前N个结果进行重新评分。

**Rescore Query具有以下特点**：

* **精准控制**：可以完全自定义二次评分的计算逻辑
* **性能优化**：只对部分结果（如前50名）进行重新计算，节省计算资源
* **灵活应用**：适用于对初步结果不满意，需要精细调整的场景
* **业务适配**：特别适合需要结合多种复杂业务规则的排序需求

#### 2.6.2 实际应用案例

**下面的例子展示了如何对图书搜索结果进行二次评分**：

```text
PUT my_index_books-demo/_bulk
{"index":{"_id":"1"}}
{"title":"ES实战","content":"ES的实战操作，实战要领，实战经验"}
{"index":{"_id":"2"}}
{"title":"MySQL实战","content":"MySQL的实战操作"}
{"index":{"_id":"3"}}
{"title":"MySQL","content":"MySQL一定要会"}

GET my_index_books-demo/_search # 普通搜索
{
  "query": {
    "match": {
      "content": "实战"
    }
  }
}

GET my_index_books-demo/_search
{
  "query": {
    "match": {
      "content": "实战"  # 查询content字段中包含"实战"的文档，权重为0.7。
    }
  },
  "rescore": {
    "query": {
      "rescore_query": {
        "match": {
          "title": "MySQL"
        }
      },
      "query_weight": 0.7,
      "rescore_query_weight": 1.2  # 对文档中title为MySQL的文档增加评分，权重为1.2，
    },
    "window_size": 50 # window_size为50，表示取分片结果的前50进行重新算分
  }
}
```

**这个查询的工作流程**：

* **第一阶段**：在content字段中搜索"实战"，获得初步结果
* **第二阶段**：对前50个结果，检查title字段是否包含"MySQL"，如果是则提升评分
* **权重平衡**：
  * query_weight: 0.7 - 第一阶段权重
  * rescore_query_weight: 1.2 - 第二阶段权重
* **最终效果**：标题包含"MySQL"且内容包含"实战"的文档会获得更高排名

**需要注意的是**，虽然rescore_query能提供更精准的结果排序，但也会增加查询的计算成本和响应时间，需要在精度和性能之间找到平衡。

## 3. 多字段搜索评分策略深度解析

### 3.1 多字段搜索的应用场景

**在实际应用中，我们经常需要在多个字段中同时搜索**，比如：
* **文章搜索**：同时在标题和正文中查找关键词
* **产品搜索**：在产品名称、描述、规格等多个字段中匹配
* **用户搜索**：在姓名、邮箱、部门等多个信息字段中查找

**核心挑战是如何设计合适的评分策略**，让最相关的结果排在前面。

### 3.2 三种核心多字段评分策略

**Elasticsearch提供了三种主要的多字段搜索策略**：

* **最佳字段（Best Fields）**：选择评分最高的字段作为文档的最终评分
  * **适用场景**：关键词应该出现在某个特定字段中才算相关
  * **典型应用**：文章搜索，关键词要么在标题中，要么在正文中

* **多数字段（Most Fields）**：将所有匹配字段的评分相加作为文档的最终评分
  * **适用场景**：关键词出现在多个字段中说明更相关
  * **典型应用**：多语言内容搜索，同义词匹配

* **跨字段（Cross Fields）**：将多个字段视为一个统一的虚拟字段进行搜索
  * **适用场景**：关键词应该分布在多个相关字段中
  * **典型应用**：个人信息搜索（姓名+地址+电话）

**选择合适的策略很重要**，因为不同的业务场景需要不同的匹配逻辑。

### 3.3 最佳字段搜索策略（Best Fields）

#### 3.3.1 基本原理与官方文档

**最佳字段策略的核心思想很直观**：如果关键词在某个字段中匹配得很好，就应该给予高分，而不需要关键词在所有字段中都出现。

**详细的技术文档可以参考**：https://www.elastic.co/guide/en/elasticsearch/reference/8.14/query-dsl-dis-max-query.html

#### 3.3.2 Bool Should查询的问题案例

**下面的例子清楚地说明了为什么需要Dis Max查询**：

```text
DELETE /blogs
PUT /blogs/_doc/1
{
  "title": "Quick brown rabbits",
  "body": "Brown rabbits are commonly seen."
}

PUT /blogs/_doc/2
{
  "title": "Keeping pets healthy",
  "body": "My quick brown fox eats rabbits on a regular basis."
}

# 查询棕色的狐狸
POST /blogs/_search
{
  "query": {
    "bool": {
      "should": [
        { "match": { "title": "Brown fox" }},
        { "match": { "body":  "Brown fox" }}
      ]
    }
  }
}
```

**这个查询的问题在于**：
* **期望结果**：文档2的body包含完整的"brown fox"，应该排在前面
* **实际结果**：文档1的分数反而更高
* **原因分析**：bool should的评分机制导致部分匹配优于完整匹配

**Bool Should的评分机制导致这个问题**：
1. **执行两个子查询**：分别在title和body中搜索"brown fox"
2. **分数相加**：将两个子查询的分数相加
3. **归一化处理**：乘以匹配语句数量，除以总语句数量

**文档1获得更高分数的原因**：
* **title字段**：匹配了"brown"
* **body字段**：匹配了"brown"和"rabbits"
* **总分效应**：两个字段都有部分匹配，分数被累加

**文档2分数较低的原因**：
* **title字段**：没有匹配任何词
* **body字段**：完整匹配"brown fox"
* **总分限制**：只有一个字段匹配，无法获得累加效应

**我们真正想要的是竞争关系**：选择匹配最好的字段分数，而不是将所有字段的分数相加。这就需要使用Dis Max查询。

#### 3.3.3 使用Dis Max实现最佳字段搜索

**Disjunction Max Query (Dis Max)专门解决这个问题**：

* **核心机制**：对每个文档，选择所有子查询中的最高分作为最终分数
* **设计理念**：字段之间是竞争关系，而不是合作关系
* **适用场景**：关键词应该集中出现在某个字段中

**具体实现如下**：

```text
POST /blogs/_search
{
  "query": {
    "dis_max": {
      "queries": [
        { "match": { "title": "Brown fox" }},
        { "match": { "body":  "Brown fox" }}
      ]
    }
  }
}
```

**使用Dis Max后的效果**：
* **文档1**：title匹配"brown"（部分匹配），body匹配"brown rabbits"（部分匹配）
* **文档2**：body完整匹配"brown fox"（完整匹配）
* **最终结果**：文档2获得更高分数，符合用户期望

#### 3.3.4 Tie Breaker参数：最佳匹配偏向度调节

**有时候我们希望介于"完全最佳"和"完全相加"之间**，Tie Breaker参数提供了这种灵活性。

**Tie Breaker的工作机制**：
* **取值范围**：0到1之间的浮点数
* **0值效果**：完全使用最佳匹配分数（等同于纯Dis Max）
* **1值效果**：所有字段同等重要（类似于Should查询）
* **中间值**：在最佳匹配基础上，给予其他匹配字段一定权重

**Tie Breaker的计算公式**：
**最终分数 = 最佳匹配字段分数 + (其他匹配字段分数 × Tie Breaker值)**

**具体应用示例**：

```text
POST /blogs/_search
{
  "query": {
    "dis_max": {
      "queries": [
        { "match": { "title": "Quick pets" }},
        { "match": { "body":  "Quick pets" }}
      ],
      "tie_breaker": 0.1  # 其他匹配字段获得10%的权重
    }
  }
}
```

**Tie Breaker = 0.1的效果**：
* **最佳匹配字段**：获得100%的权重
* **其他匹配字段**：获得10%的权重
* **平衡效果**：既突出了最佳匹配，又考虑了其他字段的贡献

#### 3.3.5 Multi Match查询的最佳字段实现

**Multi Match查询提供了更简洁的方式来实现最佳字段搜索**：

```text
POST /blogs/_search
{
  "query": {
    "multi_match": {
      "type": "best_fields",
      "query": "Brown fox",
      "fields": ["title","body"],
      "tie_breaker": 0.2
    }
  }
}
```

**这个查询等价于前面的Dis Max查询**：
* **type: "best_fields"**：指定使用最佳字段策略
* **fields**：指定要搜索的字段列表
* **tie_breaker**：控制其他字段的权重贡献

#### 3.3.6 综合案例演示

**下面的综合案例展示了最佳字段策略在复杂场景中的应用**：

```text
PUT /employee
{
  "settings": {
    "index": {
      "analysis.analyzer.default.type": "ik_max_word"
    }
  }
}

POST /employee/_bulk
{"index":{"_id":1}}
{"empId":"1","name":"员工001","age":20,"sex":"男","mobile":"19000001111","salary":23343,"deptName":"技术部","address":"湖北省武汉市洪山区光谷大厦","content":"i like to write best elasticsearch article"}
{"index":{"_id":2}}
{"empId":"2","name":"员工002","age":25,"sex":"男","mobile":"19000002222","salary":15963,"deptName":"销售部","address":"湖北省武汉市江汉路","content":"i think java is the best programming language"}
{"index":{"_id":3}}
{"empId":"3","name":"员工003","age":30,"sex":"男","mobile":"19000003333","salary":20000,"deptName":"技术部","address":"湖北省武汉市经济开发区","content":"i am only an elasticsearch beginner"}
{"index":{"_id":4}}
{"empId":"4","name":"员工004","age":20,"sex":"女","mobile":"19000004444","salary":15600,"deptName":"销售部","address":"湖北省武汉市沌口开发区","content":"elasticsearch and hadoop are all very good solution, i am a beginner"}
{"index":{"_id":5}}
{"empId":"5","name":"员工005","age":20,"sex":"男","mobile":"19000005555","salary":19665,"deptName":"测试部","address":"湖北省武汉市东湖隧道","content":"spark is best big data solution based on scala, an programming language similar to java"}
{"index":{"_id":6}}
{"empId":"6","name":"员工006","age":30,"sex":"女","mobile":"19000006666","salary":30000,"deptName":"技术部","address":"湖北省武汉市江汉路","content":"i like java developer"}
{"index":{"_id":7}}
{"empId":"7","name":"员工007","age":60,"sex":"女","mobile":"19000007777","salary":52130,"deptName":"测试部","address":"湖北省黄冈市边城区","content":"i like elasticsearch developer"}
{"index":{"_id":8}}
{"empId":"8","name":"员工008","age":19,"sex":"女","mobile":"19000008888","salary":60000,"deptName":"技术部","address":"湖北省武汉市江汉大学","content":"i like spark language"}
{"index":{"_id":9}}
{"empId":"9","name":"员工009","age":40,"sex":"男","mobile":"19000009999","salary":23000,"deptName":"销售部","address":"河南省郑州市郑州大学","content":"i like java developer"}
{"index":{"_id":10}}
{"empId":"10","name":"张湖北","age":35,"sex":"男","mobile":"19000001010","salary":18000,"deptName":"测试部","address":"湖北省武汉市东湖高新","content":"i like java developer, i also like elasticsearch"}
{"index":{"_id":11}}
{"empId":"11","name":"王河南","age":61,"sex":"男","mobile":"19000001011","salary":10000,"deptName":"销售部","address":"河南省开封市河南大学","content":"i am not like java"}
{"index":{"_id":12}}
{"empId":"12","name":"张大学","age":26,"sex":"女","mobile":"19000001012","salary":11321,"deptName":"测试部","address":"河南省开封市河南大学","content":"i am java developer, java is good"}
{"index":{"_id":13}}
{"empId":"13","name":"李江汉","age":36,"sex":"男","mobile":"19000001013","salary":11215,"deptName":"销售部","address":"河南省郑州市二七区","content":"i like java and java is very best, i like it, do you like java"}
{"index":{"_id":14}}
{"empId":"14","name":"王技术","age":45,"sex":"女","mobile":"19000001014","salary":16222,"deptName":"测试部","address":"河南省郑州市金水区","content":"i like c++"}
{"index":{"_id":15}}
{"empId":"15","name":"张测试","age":18,"sex":"男","mobile":"19000001015","salary":20000,"deptName":"技术部","address":"河南省郑州市高新开发区","content":"i think spark is good"}

GET /employee/_search
{
  "query": {
    "multi_match": {
      "query": "elasticsearch beginner 湖北省 开封市",
      "type": "best_fields",
      "fields": ["content", "address"]
    }
  },
  "size": 15
}

# 查看执行计划

GET /employee/_explain/3
{
  "query": {
    "multi_match": {
      "query": "elasticsearch beginner 湖北省 开封市",
      "type": "best_fields",
      "fields": ["content", "address"]
    }
  }
}

GET /employee/_explain/3
{
  "query": {
    "multi_match": {
      "query": "elasticsearch beginner 湖北省 开封市",
      "type": "best_fields",
      "fields": ["content", "address"],
      "tie_breaker": 0.1
    }
  }
}
```

**这个案例展示了**：
* **多字段搜索**：同时在content和address字段中搜索
* **复杂查询**：包含英文和中文关键词
* **最佳字段策略**：选择匹配最好的字段分数
* **执行计划分析**：通过Explain API理解评分过程

### 3.4 多数字段搜索策略（Most Fields）

#### 3.4.1 基本原理与实现

**多数字段策略的核心思想是**：关键词出现在越多字段中，文档越相关。

**从效果上说**，这等价于Bool Should查询，只是提供了更简洁的语法。

**具体实现方式**：

```text
GET /employee/_explain/3
{
  "query": {
    "multi_match": {
      "query": "elasticsearch beginner 湖北省 开封市",
      "type": "most_fields",
      "fields": ["content", "address"]
    }
  }
}
```

**Most Fields的评分机制**：
* **字段累加**：将所有匹配字段的分数相加
* **匹配度增强**：关键词出现在多个字段中获得更高分数
* **适用场景**：多语言内容、同义词扩展等

#### 3.4.2 不符合预期的查询案例

**下面的例子展示了一个Most Fields策略不适用的情况**：

```text
DELETE /titles
PUT /titles
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "english",
        "fields": {  # 定义 title 的另一个版本，它用了不同的分词器
          "std": {
            "type": "text",
            "analyzer": "standard"
          }
        }
      }
    }
  }
}

POST titles/_bulk
{ "index": { "_id": 1 }}
{ "title": "My dog barks" }
{ "index": { "_id": 2 }}
{ "title": "I see a lot of barking dogs on the road" }

# 结果与预期不匹配：查询查的是 title，用的是 english 分词器，做了词干提取，没有给文档 2 提高权重
GET /titles/_search
{
  "query": {
    "match": {
      "title": "barking dogs"
    }
  }
}
```

**这个案例的问题在于分词器的选择**：

**文档1的分词结果**："My dog barks"
* **English分词器**：["my", "dog", "bark"] - 提取了词干
* **Standard分词器**：["My", "dog", "barks"] - 保留原始形式

**文档2的分词结果**："I see a lot of barking dogs on the road"
* **English分词器**：["i", "see", "lot", "bark", "dog", "road"] - 词干提取
* **Standard分词器**：["I", "see", "a", "lot", "of", "barking", "dogs", "on", "the", "road"] - 原始形式

**查询"barking dogs"时的问题**：
* **用户期望**：文档2应该排在前面，因为它更贴近查询意图
* **实际结果**：English分词器将"barking"提取为"bark"，失去了准确性
* **根本原因**：只使用了一种分词器，无法兼顾准确性和召回率

#### 3.4.3 使用Most Fields优化解决方案

**解决这个问题的思路是结合两种分词器的优势**：

* **English分词器**：提高召回率，通过词干提取匹配更多相关文档
* **Standard分词器**：提高精确度，保留原始词汇形式，增强相关度

**通过Most Fields策略实现这个目标**：

```text
GET /titles/_search
{
  "query": {
    "multi_match": {
      "query": "barking dogs",
      "type": "most_fields",
      "fields": ["title", "title.std"]
    }
  }
}
```

**这个查询的工作机制**：
* **title字段**：使用English分词器，匹配"bark"和"dog"
* **title.std字段**：使用Standard分词器，匹配"barking"和"dogs"
* **分数累加**：两个字段的分数相加，文档2因更精确匹配获得更高分数

#### 3.4.4 字段权重自定义方法

**我们还可以为不同字段设置不同的权重**，让某些字段对最终评分的影响更大：

```text
GET /titles/_search
{
  "query": {
    "multi_match": {
      "query": "barking dogs",
      "type": "most_fields",
      "fields": ["title^2", "title.std"] # 把 title 字段的权重增加到 2
    }
  }
}
```

**权重设置的效果**：
* **title字段**：权重提升2倍，对最终评分影响更大
* **title.std字段**：使用默认权重1倍
* **平衡策略**：既保证了召回率，又突出了精确匹配的重要性

### 3.5 跨字段搜索策略（Cross Fields）

#### 3.5.1 基本概念与原理

**跨字段策略的核心思想是**：将多个字段合并成一个虚拟字段进行搜索，关键词可以分布在不同的相关字段中。

**Cross Fields的工作机制**：
* **字段合并**：将指定字段的内容合并在一起
* **统一分词**：对合并后的内容进行统一分词和搜索
* **整体匹配**：关键词可以跨字段匹配，视为一个整体

**适用场景包括**：
* **个人信息搜索**：姓名、地址、电话等信息分散在多个字段
* **产品信息搜索**：产品名、品牌、规格等分布在相关字段
* **地理位置搜索**：省、市、区、详细地址等字段组合

#### 3.5.2 不符合预期的查询案例

**下面的例子说明了为什么需要Cross Fields策略**：

```text
DELETE /address
PUT /address
{
  "settings": {
    "index": {
      "analysis.analyzer.default.type": "ik_max_word"
    }
  }
}

PUT /address/_bulk
{ "index": { "_id": "1" }}
{"province": "湖南","city": "长沙"}
{ "index": { "_id": "2" }}
{"province": "湖南","city": "常德"}
{ "index": { "_id": "3" }}
{"province": "广东","city": "广州"}
{ "index": { "_id": "4" }}
{"province": "湖南","city": "邵阳"}

# 使用 most_fields 不符合预期，它会先对查询条件"湖南常德"进行分词，然后分别与 provience 字段、city 字段进行相似度匹配，最后再把两个字段的分数进行加总。

# 它不能指定查询条件的匹配方式（即 operator 是 and 还是 or），这不是我们期望的。

GET /address/_search
{
  "query": {
    "multi_match": {
      "query": "湖南常德",
      "type": "most_fields",
      "fields": ["province", "city"]
    }
  }
}
```

**使用Most Fields搜索"湖南常德"的问题**：

* **查询词分词**：["湖南", "常德"]
* **字段匹配**：
  * province字段匹配"湖南"
  * city字段匹配"常德"
* **结果问题**：
  * 文档1：province="湖南", city="长沙" - 匹配"湖南"
  * 文档2：province="湖南", city="常德" - 匹配"湖南"和"常德"
  * 文档4：province="湖南", city="邵阳" - 匹配"湖南"
* **不理想结果**：文档1和文档4也会返回，因为它们匹配了"湖南"

**用户期望的精确匹配**：
* **完整匹配**：需要同时包含"湖南"和"常德"
* **精确结果**：只有文档2应该返回
* **Most Fields局限**：无法指定AND操作符来要求所有分词都必须匹配

#### 3.5.3 Cross Fields解决方案

**Cross Fields策略完美解决了这个问题**：

```text
GET /address/_search
{
  "query": {
    "multi_match": {
      "query": "湖南常德",
      "type": "cross_fields",
      "operator": "and",
      "fields": ["province", "city"]
    }
  }
}
```

**Cross Fields的工作机制**：

* **字段合并**：将province和city字段内容合并为虚拟字段
  * 文档1：["湖南", "长沙"]
  * 文档2：["湖南", "常德"]
  * 文档3：["广东", "广州"]
  * 文档4：["湖南", "邵阳"]
* **AND操作符**：要求查询词"湖南"和"常德"都必须在虚拟字段中匹配
* **精确结果**：只有文档2（"湖南" + "常德"）完全匹配

**Cross Fields的优势**：
* **精确匹配**：通过AND操作符确保所有查询词都匹配
* **跨字段灵活**：关键词可以分布在不同字段中
* **用户友好**：符合用户对地址搜索的直观期望

#### 3.5.4 Copy To替代方案

**除了Cross Fields，还可以使用Copy To策略**：

```text
DELETE /address
PUT /address
{
  "mappings": {
    "properties": {
      "province": {
        "type": "keyword",
        "copy_to": "full_address"
      },
      "city": {
        "type": "text",
        "copy_to": "full_address"
      }
    }
  },
  "settings": {
    "index": {
      "analysis.analyzer.default.type": "ik_max_word"
    }
  }
}

PUT /address/_bulk
{ "index": { "_id": "1" }}
{"province": "湖南","city": "长沙"}
{ "index": { "_id": "2" }}
{"province": "湖南","city": "常德"}
{ "index": { "_id": "3" }}
{"province": "广东","city": "广州"}
{ "index": { "_id": "4" }}
{"province": "湖南","city": "邵阳"}

GET /address/_search
{
  "query": {
    "match": {
      "full_address": {
        "query": "湖南常德",
        "operator": "and"
      }
    }
  }
}
```

**Copy To策略的特点**：

* **索引时合并**：在文档索引时自动将指定字段复制到目标字段
* **存储开销**：需要额外的存储空间保存合并后的字段
* **查询简化**：查询时直接对合并字段进行搜索
* **性能考虑**：索引时开销增加，查询时性能较好

**两种方案的对比**：

* **Cross Fields**：
  * **优势**：无需额外存储，查询时灵活
  * **劣势**：查询时计算开销较大

* **Copy To**：
  * **优势**：查询性能好，逻辑简单
  * **劣势**：需要额外存储空间，索引时开销增加

**选择建议**：
* **数据量小**：Copy To更简单
* **数据量大**：Cross Fields更节省存储
* **查询频繁**：Copy To性能更好
* **存储敏感**：Cross Fields更经济