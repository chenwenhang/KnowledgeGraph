## 数据集说明

* 来源：[军事新闻数据集](https://download.csdn.net/download/qq_36152012/10756072)

* 数据集格式
```
{   
	"article_id": 287071,  // 问题的数字ID  
	"article_type": "防务快讯",  // 文章类型字符串   
  	"article_title": "标题",  // 文章标题字符串   
  	"article_content": "正文内容",  // 文章正文内容字符串   
  	"questions": [//问题列表  
  		{ 
  			"questions_id":"问题id",//问题 
  			"question":"问题1xxx",//问题 
  			"answer":"答案1xxx",//答案
   			"question_type":"问题类型1"// 问题类型字符串 
   		}, { 
   			"questions_id":"问题id",//问题 
   			"question":"问题2xxx", 
			"answer":"答案2xxx", 
			"question_type":"问题类型2" 
		}
	]   
}
```