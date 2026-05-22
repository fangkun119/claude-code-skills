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

当用户使用搜索引擎时，他们通常会期望搜索结果满足四个关键要求。首先是信息完整性，用户希望能够找到所有相关的内容，不遗漏任何重要信息。其次是结果准确性，用户希望返回的结果中不相关的内容越少越好，这样才能快速定位真正需要的信息。第三是评分合理性，文档的相关性评分应该准确反映其与查询的匹配程度，让用户对结果有合理的预期。最后是业务适配性，排序结果要符合具体的业务需求和用户偏好，这样才能真正解决用户的实际问题。

Elasticsearch通过相关性分数(_score)来量化文档与查询的匹配程度，这是一个非常实用的机制。评分越高说明相关性越强，用户就越容易找到想要的内容。这种评分机制让搜索不再是简单的匹配游戏，而是变成了一个智能化的内容推荐过程。

让我们通过一个具体的例子来理解这个概念。假设用户搜索"JAVA多线程设计模式"，这个查询会被分词成三个关键词：JAVA、设计模式和多线程。每个关键词都能匹配到不同的文档，我们可以通过下表清楚地看到文档2和文档3的相关性更高：

| 关键词   | 文档ID      |
| :------- | :---------- |
| JAVA     | 1,2,3       |
| 设计模式 | 1,2,3,4,5,6 |
| 多线程   | 2,3,7,9     |

虽然Elasticsearch提供了默认的相关性计算方法，但它的真正优势在于允许用户根据特定的业务需求来自定义相关性计算。这种灵活性让搜索结果能够更符合实际使用场景，为用户提供更加精准和个性化的搜索体验。

### 1.2 Elasticsearch相关性评分机制

#### 1.2.1 实用评分函数的工作原理

Elasticsearch采用了一种非常聪明的两阶段评分方法来平衡准确性和性能。第一阶段使用布尔模型快速筛选出匹配的文档，这个过程就像是初步筛选，把可能相关的文档找出来。第二阶段通过"实用评分函数"精确计算每个文档的相关性分数，这个阶段会仔细分析文档与查询的匹配程度，给出精确的评分。

这个评分公式融合了多种先进技术，体现了搜索算法的演进历程。它借鉴了经典的TF-IDF（词频-逆向文档频率）和向量空间模型作为理论基础，同时加入了协调因子、字段长度归一化、词权重提升等现代优化特性。在算法演进方面，Elasticsearch 5之前使用TF-IDF算法，5之后升级到更先进的Okapi BM25算法，这个升级显著提升了搜索的相关性准确性。

说到BM25算法，它的名称含义很有意思。BM代表"Best Match"（最佳匹配），而25表示经过25次迭代优化得出的最终版本。相比TF-IDF，BM25在保持准确性的同时增加了更多可调参数，使得算法更加强大和实用，能够适应不同的搜索场景和业务需求。

#### 1.2.2 TF-IDF与BM25算法对比

TF-IDF和BM25这两种算法都基于相同的核心假设，这些假设在信息检索领域被证明是非常有效的。第一个假设是稀有词更重要，算法通过逆向文档频率来区分普通词汇（如"的"、"是"）和专业词汇。第二个假设是频率反映相关性，即词在文档中出现频率越高，相关性通常越强。

从逻辑角度看，这个假设非常直观。在文档内部，某个词出现得越频繁，说明这个文档越可能与该主题相关。但是从跨文档的角度看，某个词在所有文档中出现得越频繁，说明它越通用，权重应该越低。综合起来，越罕见的词在当前文档中频繁出现，就越能代表这个文档的核心主题。

BM25相比TF-IDF有了显著的改进，主要体现在两个方面。首先，BM25增加了可调节的参数，使算法更加强大和实用，能够根据不同场景进行优化调整。其次，BM25引入了饱和机制，在TF-IDF中词频越高分数就越高，而BM25的分数会趋于一个饱和值，避免了某个词过度影响评分，使得评分更加均衡和合理。

#### 1.2.3 TF-IDF核心组件详解

TF-IDF算法由三个核心组件构成，它们在索引时计算并存储，最终组合成单个词的权重。这三个组件分别是词频（TF）、逆向文档频率（IDF）和字段长度归一值（Field-length Norm）。

词频（TF - Term Frequency）的基本原理是检索词在文档中出现的次数越多，相关性越高。计算公式非常简单：TF = 某个词在文档中的出现次数 ÷ 文档的总词数。这样设计的效果是确保包含更多搜索词的文档获得更高分数，这在实际应用中非常有效。

逆向文档频率（IDF - Inverse Document Frequency）的核心理念是在所有文档中越常见的词，重要性越低。计算逻辑是：IDF = log(语料库文档总数 ÷ (包含该词的文档数 + 1))。这种设计降低了"的"、"是"、"在"等通用词的权重，提升了专业词汇的重要性，使得搜索结果更加精准。

字段长度归一值（Field-length Norm）的设计思想是短字段中的匹配比长字段中的匹配更有意义。例如，搜索词出现在标题字段比出现在正文字段应该获得更高权重，因为标题通常更能代表文档的核心主题。这种机制确保精确匹配不被长文档稀释，提高了搜索的准确性。

#### 1.2.4 使用Explain API查看TF-IDF评分详情

Elasticsearch提供了一个非常实用的Explain API来帮助开发者理解评分机制。通过这个API，你可以清楚地看到每个文档的详细评分过程、每个词对总分的贡献以及各种评分因素的具体数值。

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

通过Explain API，你可以清楚地看到每个文档的详细评分过程、每个词对总分的贡献以及各种评分因素的具体数值。这对于调试搜索问题、优化相关性评分非常有帮助。

### 1.3 自定义相关性评分的必要性与应用

#### 1.3.1 自定义评分的主要应用场景

自定义相关性评分通过修改Elasticsearch的默认评分计算，让最符合用户期望的结果排在前面，从而满足特定应用场景的需求。这种定制化的能力让搜索引擎能够更好地服务于特定的业务目标和用户需求。

自定义评分在四个场景中特别有价值。首先是个性化排序偏好，根据用户习惯调整搜索结果的排序，让不同用户看到最适合自己的结果。其次是业务字段权重优化，给重要字段（如商品标题、价格）赋予更高权重，让业务关键因素影响排序。第三是复杂业务逻辑集成，将库存状态、促销活动等业务因素融入评分逻辑。最后是用户行为数据融合，利用点击率、购买转化率等用户行为数据优化搜索体验。

#### 1.3.2 自定义评分的战略意义

搜索引擎的本质是一个匹配过程，目标是从海量数据中精准找到满足用户需求的内容。这个过程看起来简单，但实际上充满了挑战。相关性判断一直是搜索引擎领域的核心挑战，主要因为用户意图复杂、内容多样性强、场景差异大等因素的影响。

用户查询往往很简短，但背后有复杂的真实需求。比如用户搜索"苹果"，可能想要苹果公司的产品，也可能想要苹果这种水果，甚至可能想要苹果公司的股票信息。同时，网页、文档、商品等不同类型内容需要不同的相关性标准，学术搜索和商品搜索的相关性标准也完全不同。

如果搜索引擎不能准确理解用户意图，将相关结果排在前面，就会严重影响用户体验和满意度。这就是为什么自定义相关性评分如此重要的根本原因。通过自定义评分，我们可以让搜索引擎更好地理解用户意图，提供更加精准和个性化的搜索结果。

## 2. 自定义评分策略体系与实现方法

### 2.1 自定义评分策略的整体架构

实现自定义评分策略可以从三个层面入手，每个层面都有其独特的优势和适用场景。索引层面是在数据存储时就影响相关性计算，这种方式对查询性能影响最小，但灵活性相对较低。查询层面是在执行搜索时动态调整评分，这种方式提供了最大的灵活性，但可能对查询性能有一定影响。后处理层面是对初步结果进行二次优化，这种方式可以在不改变底层评分机制的情况下实现复杂的排序逻辑。

Elasticsearch提供了五种主要的自定义评分策略，每种策略都针对不同的使用场景。Index Boost是在索引层面为不同索引设置不同权重，适合跨索引搜索的场景。Boosting是为不同查询条件设置不同的权重系数，这是最常用的自定义评分方式。Negative Boost是对满足特定条件的结果进行降权处理，提供了一种温和的过滤方式。Function Score是通过自定义函数实现复杂的评分逻辑，这是最强大但也最复杂的策略。Rescore Query是对查询结果进行二次评分和重新排序，适合需要精细调整的场景。

### 2.2 Index Boost策略：跨索引权重分配

#### 2.2.1 应用场景与原理

Index Boost策略特别适合跨索引搜索的场景，比如搜索包含多种类型数据的系统。一个典型的实际应用是一批数据包含不同标签，数据结构相同，需要将不同标签存储在不同索引中，并按标签优先级展示结果。例如，A类数据优先展示，然后是B类，最后是C类。

这种策略的优势在于它不需要修改查询逻辑，只需要在搜索请求中指定不同索引的权重即可。这对于需要处理大量历史数据的系统特别有用，可以确保最新的或最重要的数据优先展示，同时保持对历史数据的访问能力。

#### 2.2.2 具体实现示例

下面通过一个完整的示例来演示Index Boost的实现。我们创建三个不同的索引，分别代表不同优先级的数据，然后通过indices_boost参数来控制它们的权重。

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

通过indices_boost参数，我们可以精确控制不同索引的权重。在这个例子中，my_index_100a的权重提升1.5倍，具有最高优先级；my_index_100b的权重提升1.2倍，具有中等优先级；而my_index_100c使用默认权重，具有最低优先级。这样确保了符合用户期望的排序结果。

### 2.3 Boosting策略：查询条件权重优化

#### 2.3.1 工作机制与参数说明

Boosting策略的核心思想是当有多个查询条件时，为不同条件设置不同的权重系数，影响最终的相关性评分。这种方法非常直观且易于理解，让开发者能够精确控制不同因素对最终评分的影响。

boosting参数的取值规则很直观。0-1之间的值表示降权处理，比如0.2表示降低到原来的20%。大于1的值表示提升权重，比如1.5表示提升到原来的150%。这种灵活的权重设置让开发者能够根据业务需求精确调整搜索结果的排序。

#### 2.3.2 实际应用示例

下面的例子展示了如何为标题和内容字段设置不同权重。在大多数内容搜索场景中，标题中的关键词匹配比内容中的匹配更重要，因此我们应该给标题匹配更高的权重。

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

在这个查询中，标题匹配的权重提升4倍，说明标题中的关键词更重要；内容匹配使用默认权重1倍。实际效果是标题中包含"apple,ipad"的文档会获得更高分数，这符合用户的搜索预期，因为标题通常更能代表文档的核心主题。

### 2.4 Negative Boost策略：选择性降权处理

#### 2.4.1 原理与使用场景

Negative Boost提供了一种温和的过滤方式，当某些结果不完全符合要求，但又不想完全排除它们时，可以通过降低权重来处理。这种方法比完全过滤更加灵活，能够在保证搜索结果质量的同时保留一定的多样性。

Negative Boost的工作机制很巧妙。它只对查询中定义为negative的部分生效，给命中negative条件的文档乘以一个小于1的系数（如0.3），从而降低这些文档的最终评分。但重要的是，这些文档仍然可以出现在搜索结果中，只是位置会相对靠后。

一个经典的应用场景是苹果公司产品搜索。当用户搜索"apple"时，通常希望优先看到苹果公司的产品，但不想完全排除"apple pie"等相关内容。如果使用must_not查询，会完全过滤掉"apple pie"等不相关内容，这可能过于严格。而使用Negative Boost，可以降低"apple pie"等内容的权重，让它们排在后面，但仍然可见，这样既保证了主要内容的优先级，又保留了相关内容的可见性。

#### 2.4.2 实现对比示例

下面的代码对比了三种不同的处理方式：普通搜索、使用must_not排除和使用negative_boost降权。通过这个对比，我们可以清楚地看到不同策略的效果差异。

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

三种方案的对比效果很明显。普通搜索会包含"apple pie"的文档正常显示。Must Not方案会完全排除包含"pie"的文档，结果可能过于严格。而Negative Boost方案会降低包含"pie"文档的权重到20%，让苹果公司产品优先显示，但相关内容仍然可见，这种平衡的方式在大多数情况下是最佳选择。

### 2.5 Function Score策略：自定义评分公式

#### 2.5.1 功能特点与应用场景

Function Score是最强大的自定义评分策略，它允许用户通过自定义查询语句和脚本，实现高度个性化的排序控制。这种策略的强大之处在于它几乎可以实现任何你能想到的评分逻辑，只要你能用数学公式或脚本表达出来。

Function Score特别适合复杂的业务场景。在电商商品排序中，可以结合相关性评分、销量、用户评价等多个因素来确定最终排序。在内容推荐中，可以考虑用户兴趣、内容热度、时效性等维度。在地理位置搜索中，可以结合距离、评分、可用性等因素。这些复杂的需求通过Function Score都可以轻松实现。

以商品搜索为例，除了文字相关性，我们可能还希望根据销量和浏览人数来调整排序权重。考虑以下商品数据：商品A销量10、浏览人数10；商品B销量20、浏览人数20。我们可以设计这样的评分公式：最终评分 = 原始相关性评分 × (销量 + 浏览人数)。

这个设计的优势在于它不仅考虑了文本匹配度，还融入了商业指标，使得销量和浏览人数高的商品获得更高排名。这种业务导向的设计能够提高用户的购买转化率，因为热销商品通常更符合大多数用户的需求和偏好。

#### 2.5.2 Script Score实现方式

通过Script Score，我们可以实现上述的自定义评分逻辑。Script Score允许我们使用脚本语言来定义评分公式，这提供了极大的灵活性。

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

这个查询的工作原理很清晰。基础查询使用match_all获取所有商品，评分脚本使用`_score*(doc['sales'].value+doc['visitors'].value)`来计算最终分数。计算过程是原始相关性分数乘以（销量加浏览人数），最终效果是商品C (30+30=60) > 商品B (20+20=40) > 商品A (10+10=20)。这种排序方式更符合商业逻辑，有助于提高用户转化率。

### 2.6 Rescore Query策略：二次评分优化

#### 2.6.1 二次评分的工作原理

Rescore Query提供了两阶段评分的机制，先进行初步搜索，然后对前N个结果进行重新评分。这种策略特别适合需要对初步结果进行精细调整的场景，能够在保证查询性能的同时提供更精准的排序结果。

Rescore Query具有以下特点。它可以完全自定义二次评分的计算逻辑，提供了极大的灵活性。同时，由于只对部分结果（如前50名）进行重新计算，能够节省计算资源，在精度和性能之间找到平衡。它特别适合需要结合多种复杂业务规则的排序需求，能够实现比单次评分更复杂的排序逻辑。

#### 2.6.2 实际应用案例

下面的例子展示了如何对图书搜索结果进行二次评分。在这个例子中，我们首先在content字段中搜索"实战"，然后对前50个结果检查title字段是否包含"MySQL"，如果是则提升评分。

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

这个查询的工作流程分为两个阶段。第一阶段在content字段中搜索"实战"，获得初步结果。第二阶段对前50个结果，检查title字段是否包含"MySQL"，如果是则提升评分。权重平衡方面，query_weight设为0.7作为第一阶段权重，rescore_query_weight设为1.2作为第二阶段权重。最终效果是标题包含"MySQL"且内容包含"实战"的文档会获得更高排名，这更符合用户的搜索意图。

需要注意的是，虽然rescore_query能提供更精准的结果排序，但也会增加查询的计算成本和响应时间。在实际应用中，需要在精度和性能之间找到合适的平衡点。

## 3. 多字段搜索评分策略深度解析

### 3.1 多字段搜索的应用场景

在实际应用中，我们经常需要在多个字段中同时搜索，这种需求非常普遍。在文章搜索中，我们可能需要在标题和正文中同时查找关键词。在产品搜索中，我们可能需要在产品名称、描述、规格等多个字段中进行匹配。在用户搜索中，我们可能在姓名、邮箱、部门等多个信息字段中查找用户信息。

核心挑战是如何设计合适的评分策略，让最相关的结果排在前面。不同的业务场景需要不同的匹配逻辑，有些场景希望关键词集中出现在某个字段中，有些场景希望关键词分散在多个字段中，还有些场景希望关键词能够跨字段匹配。理解这些差异并选择合适的策略对于提供高质量的搜索体验至关重要。

### 3.2 三种核心多字段评分策略

Elasticsearch提供了三种主要的多字段搜索策略，每种策略都有其独特的优势和适用场景。

最佳字段（Best Fields）策略选择评分最高的字段作为文档的最终评分。这种策略适用于关键词应该出现在某个特定字段中才算相关的场景，比如文章搜索中关键词要么在标题中，要么在正文中。它的优势是能够突出最佳匹配，避免部分匹配的干扰。

多数字段（Most Fields）策略将所有匹配字段的评分相加作为文档的最终评分。这种策略适用于关键词出现在多个字段中说明更相关的场景，比如多语言内容搜索、同义词匹配等。它的优势是能够综合考虑多个字段的匹配情况，提高匹配的全面性。

跨字段（Cross Fields）策略将多个字段视为一个统一的虚拟字段进行搜索。这种策略适用于关键词应该分布在多个相关字段中的场景，比如个人信息搜索（姓名+地址+电话）。它的优势是能够实现跨字段的灵活匹配，符合用户对复合信息的搜索期望。

选择合适的策略很重要，因为不同的业务场景需要不同的匹配逻辑。理解每种策略的工作原理和适用场景，能够帮助我们设计出更符合用户需求的搜索系统。

### 3.3 最佳字段搜索策略（Best Fields）

#### 3.3.1 基本原理与官方文档

最佳字段策略的核心思想很直观：如果关键词在某个字段中匹配得很好，就应该给予高分，而不需要关键词在所有字段中都出现。这种策略模拟了人类的直觉判断，当我们搜索时，如果某个字段完全匹配了我们的查询，我们就会认为这个结果很相关，即使其他字段没有匹配。

详细的技术文档可以参考Elasticsearch官方文档：https://www.elastic.co/guide/en/elasticsearch/reference/8.14/query-dsl-dis-max-query.html。官方文档提供了详细的技术说明和示例，对于深入理解这个策略非常有帮助。

#### 3.3.2 Bool Should查询的问题案例

下面的例子清楚地说明了为什么需要Dis Max查询。我们创建两个文档，一个文档的title包含"Quick brown rabbits"，body包含"Brown rabbits are commonly seen."；另一个文档的title包含"Keeping pets healthy"，body包含"My quick brown fox eats rabbits on a regular basis."。当我们搜索"brown fox"时，期望文档2排在前面，因为它的body包含了完整的"brown fox"。

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

但这个查询的结果与预期不符，文档1的分数反而更高。原因是bool should的评分机制导致部分匹配优于完整匹配。Bool Should会执行两个子查询，分别在title和body中搜索"brown fox"，然后将两个子查询的分数相加，最后乘以匹配语句数量，除以总语句数量进行归一化处理。

文档1获得更高分数的原因是title字段匹配了"brown"，body字段匹配了"brown"和"rabbits"，两个字段都有部分匹配，分数被累加。而文档2只有body字段完整匹配"brown fox"，title字段没有匹配任何词，无法获得累加效应。这种评分机制与用户的直觉不符，我们需要一种能够选择最佳匹配字段分数的机制。

#### 3.3.3 使用Dis Max实现最佳字段搜索

Disjunction Max Query (Dis Max)专门解决这个问题。它的核心机制是对每个文档，选择所有子查询中的最高分作为最终分数。这种设计理念是字段之间是竞争关系，而不是合作关系，适用于关键词应该集中出现在某个字段中的场景。

具体实现如下：

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

使用Dis Max后的效果符合用户期望。文档1的title匹配"brown"（部分匹配），body匹配"brown rabbits"（部分匹配）；文档2的body完整匹配"brown fox"（完整匹配）。最终文档2获得更高分数，因为它的最佳匹配字段分数更高。

#### 3.3.4 Tie Breaker参数：最佳匹配偏向度调节

有时候我们希望介于"完全最佳"和"完全相加"之间，Tie Breaker参数提供了这种灵活性。Tie Breaker的取值范围是0到1之间的浮点数，0值效果是完全使用最佳匹配分数（等同于纯Dis Max），1值效果是所有字段同等重要（类似于Should查询），中间值则在最佳匹配基础上，给予其他匹配字段一定权重。

Tie Breaker的计算公式是：最终分数 = 最佳匹配字段分数 + (其他匹配字段分数 × Tie Breaker值)。这种设计让我们能够在突出最佳匹配的同时，也考虑其他字段的贡献。

具体应用示例：

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

当Tie Breaker = 0.1时，最佳匹配字段获得100%的权重，其他匹配字段获得10%的权重。这种平衡效果既突出了最佳匹配，又考虑了其他字段的贡献，通常能够提供更好的搜索体验。

#### 3.3.5 Multi Match查询的最佳字段实现

Multi Match查询提供了更简洁的方式来实现最佳字段搜索，它封装了Dis Max的复杂性，提供了更易用的接口。

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

这个查询等价于前面的Dis Max查询。type: "best_fields"指定使用最佳字段策略，fields指定要搜索的字段列表，tie_breaker控制其他字段的权重贡献。Multi Match查询的语法更加简洁，是实际开发中常用的方式。

#### 3.3.6 综合案例演示

下面的综合案例展示了最佳字段策略在复杂场景中的应用。我们创建一个员工信息索引，包含员工的详细信息，然后进行多字段搜索。

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

这个案例展示了多字段搜索的复杂应用场景。我们同时在content和address字段中搜索，查询包含英文和中文关键词，使用最佳字段策略选择匹配最好的字段分数，并通过Explain API分析评分过程。这种综合应用展示了最佳字段策略在实际业务中的强大功能。

### 3.4 多数字段搜索策略（Most Fields）

#### 3.4.1 基本原理与实现

多数字段策略的核心思想是关键词出现在越多字段中，文档越相关。从效果上说，这等价于Bool Should查询，只是提供了更简洁的语法。这种策略特别适合需要综合多个字段匹配情况的场景。

具体实现方式非常简单，只需将type设置为"most_fields"即可：

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

Most Fields的评分机制是将所有匹配字段的分数相加，使得关键词出现在多个字段中获得更高分数。这种策略适用于多语言内容、同义词扩展等场景，能够提高匹配的全面性和准确性。

#### 3.4.2 不符合预期的查询案例

下面的例子展示了一个Most Fields策略不适用的情况。我们创建一个titles索引，使用两种不同的分词器对title字段进行处理，然后搜索"barking dogs"。

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

这个案例的问题在于分词器的选择。文档1"My dog barks"使用English分词器会被分词为["my", "dog", "bark"]（提取了词干），使用Standard分词器会被分词为["My", "dog", "barks"]（保留原始形式）。文档2"I see a lot of barking dogs on the road"使用English分词器会被分词为["i", "see", "lot", "bark", "dog", "road"]（词干提取），使用Standard分词器会被分词为["I", "see", "a", "lot", "of", "barking", "dogs", "on", "the", "road"]（原始形式）。

当查询"barking dogs"时，用户期望文档2应该排在前面，因为它更贴近查询意图。但实际结果是English分词器将"barking"提取为"bark"，失去了准确性。根本原因是只使用了一种分词器，无法兼顾准确性和召回率。

#### 3.4.3 使用Most Fields优化解决方案

解决这个问题的思路是结合两种分词器的优势。English分词器可以提高召回率，通过词干提取匹配更多相关文档。Standard分词器可以提高精确度，保留原始词汇形式，增强相关度。

通过Most Fields策略实现这个目标：

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

这个查询的工作机制是title字段使用English分词器，匹配"bark"和"dog"；title.std字段使用Standard分词器，匹配"barking"和"dogs"；然后将两个字段的分数相加，文档2因更精确匹配获得更高分数。这种结合方式既保证了召回率，又提高了精确度。

#### 3.4.4 字段权重自定义方法

我们还可以为不同字段设置不同的权重，让某些字段对最终评分的影响更大：

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

权重设置的效果是title字段权重提升2倍，对最终评分影响更大；title.std字段使用默认权重1倍。这种平衡策略既保证了召回率，又突出了精确匹配的重要性，通常能够提供更好的搜索体验。

### 3.5 跨字段搜索策略（Cross Fields）

#### 3.5.1 基本概念与原理

跨字段策略的核心思想是将多个字段合并成一个虚拟字段进行搜索，关键词可以分布在不同的相关字段中。这种策略模拟了用户对复合信息的搜索期望，比如搜索地址时，用户可能期望"湖南常德"能够匹配到省份为"湖南"、城市为"常德"的记录。

Cross Fields的工作机制是将指定字段的内容合并在一起，对合并后的内容进行统一分词和搜索，关键词可以跨字段匹配，视为一个整体。这种策略适用于个人信息搜索（姓名、地址、电话等信息分散在多个字段）、产品信息搜索（产品名、品牌、规格等分布在相关字段）、地理位置搜索（省、市、区、详细地址等字段组合）等场景。

#### 3.5.2 不符合预期的查询案例

下面的例子说明了为什么需要Cross Fields策略。我们创建一个地址索引，包含省份和城市字段，然后搜索"湖南常德"。

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

使用Most Fields搜索"湖南常德"时，查询词被分词为["湖南", "常德"]。province字段匹配"湖南"，city字段匹配"常德"。结果问题是文档1（province="湖南", city="长沙"）匹配"湖南"，文档2（province="湖南", city="常德"）匹配"湖南"和"常德"，文档4（province="湖南", city="邵阳"）匹配"湖南"。不理想的结果是文档1和文档4也会返回，因为它们匹配了"湖南"。

用户期望的精确匹配是需要同时包含"湖南"和"常德"，只有文档2应该返回。Most Fields的局限在于无法指定AND操作符来要求所有分词都必须匹配，这导致了不够精确的搜索结果。

#### 3.5.3 Cross Fields解决方案

Cross Fields策略完美解决了这个问题：

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

Cross Fields的工作机制是将province和city字段内容合并为虚拟字段。文档1为["湖南", "长沙"]，文档2为["湖南", "常德"]，文档3为["广东", "广州"]，文档4为["湖南", "邵阳"]。通过AND操作符要求查询词"湖南"和"常德"都必须在虚拟字段中匹配，最终只有文档2（"湖南" + "常德"）完全匹配。

Cross Fields的优势在于通过AND操作符确保所有查询词都匹配，同时允许关键词分布在不同字段中，符合用户对地址搜索的直观期望。

#### 3.5.4 Copy To替代方案

除了Cross Fields，还可以使用Copy To策略：

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

Copy To策略的特点是在文档索引时自动将指定字段复制到目标字段，需要额外的存储空间保存合并后的字段。查询时直接对合并字段进行搜索，逻辑简单，性能较好。但索引时开销增加，需要权衡存储和查询性能。

两种方案的对比：Cross Fields无需额外存储，查询时灵活，但查询时计算开销较大。Copy To查询性能好，逻辑简单，但需要额外存储空间，索引时开销增加。

选择建议：数据量小时Copy To更简单，数据量大时Cross Fields更节省存储，查询频繁时Copy To性能更好，存储敏感时Cross Fields更经济。