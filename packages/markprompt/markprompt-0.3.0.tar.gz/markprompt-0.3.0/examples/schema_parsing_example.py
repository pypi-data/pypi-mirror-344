"""
使用 MarkPrompt 的 response_format 和 schema 解析功能的示例。
"""

import os
import json
from typing import List, Optional
from pydantic import BaseModel, Field

from openai import OpenAI

from markprompt import MarkPromptClient
from markprompt.core.logger import setup_logger

# 配置日志
logger = setup_logger(__name__)

# OpenAI配置
api_key = os.environ.get("OPENAI_API_KEY", "sk-...")  # 替换为你的API密钥
base_url = "http://127.0.0.1:10240/v1"  # 或你的自定义基础URL

openai = OpenAI()

# 定义响应模型
class MovieReview(BaseModel):
    """电影评论结构"""
    title: str = Field(description="电影标题")
    year: int = Field(description="电影发行年份")
    rating: float = Field(description="评分（0-10）")
    review: str = Field(description="评论内容")
    pros: List[str] = Field(description="优点列表")
    cons: List[str] = Field(description="缺点列表")
    recommended: bool = Field(description="是否推荐")
    suitable_for: Optional[List[str]] = Field(None, description="适合人群")


# 定义简单的模板内容（由于无法访问 prompts 目录，这里直接使用字符串）
template_content = """---
metadata:
  name: 电影评论家
  description: 根据用户输入的电影名称生成详细评论
provider:
  name: default
generation_config:
  model: gpt-4.1
  temperature: 0.7
---

你是一个专业电影评论家。请根据用户提供的电影名称，提供详细的评论。

system:
请以专业电影评论家的身份，根据用户提供的电影名称，编写一篇详细的评论。

user:
{{user_input}}
"""


def demonstrate_schema_parsing():
    """演示 Schema 解析功能"""
    # 创建一个临时模板文件
    import tempfile
    import inspect
    import json  # 在函数内部再次导入以确保访问
    
    # 打印调试信息
    print("\n===== MovieReview 类信息 =====")
    print(f"MovieReview 是否是 BaseModel 的子类: {issubclass(MovieReview, BaseModel)}")
    print(f"MovieReview.__class__.__name__: {MovieReview.__class__.__name__}")
    print(f"MovieReview 类的 MRO: {[cls.__name__ for cls in MovieReview.mro()]}")
    print(f"MovieReview Schema: {json.dumps(MovieReview.model_json_schema(), indent=2, ensure_ascii=False)}")
    print("\n")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # 写入模板文件
        template_path = os.path.join(temp_dir, "movie_reviewer.md")
        with open(template_path, "w", encoding="utf-8") as f:
            f.write(template_content)
        
        # 创建客户端
        client = MarkPromptClient(
            template_dir=temp_dir,
            client=openai
        )
       
        try:
            # 准备用户问题
            user_question = "请评价电影《泰坦尼克号》"
            user_question = {
                "role": "user",
                "content": user_question
            }
            user_question = {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_question
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://s3.us-west-2.amazonaws.com/huami-public-us2/PICTURE/com.xiaomi.hm.health/3089641436/image_1740015785_5f497e69.jpeg"
                        }
                    }
                ]
            }
            user_question = [
                    {
                        "type": "text",
                        "text": "请评价电影《泰坦尼克号》"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://s3.us-west-2.amazonaws.com/huami-public-us2/PICTURE/com.xiaomi.hm.health/3089641436/image_1740015785_5f497e69.jpeg"
                        }
                    }
                ]

            # 使用 schema 解析
            print("\n正在生成带结构的电影评论...")
            try:
                response = client.generate_beta(
                    "movie_reviewer",  # 使用电影评论模板
                    user_question,  # 用户问题
                    response_format=MovieReview,  # 传递 BaseModel
                    verbose=True  # 启用详细日志
                )
            except Exception as e:
                print(f"生成过程中出现错误: {e}")
                # 尝试使用 JSON 模式提供更多信息
                response = client.generate(
                    "movie_reviewer",  # 使用电影评论模板
                    user_question,  # 用户问题
                    response_format={"type": "json_object", "schema": MovieReview.model_json_schema()},
                    verbose=True  # 启用详细日志
                )
            
            # 输出结果
            print("\n===== 结构化电影评论 =====")
            print(f"\n返回类型: {type(response)}")
            print(f"\n返回内容: {response}")
            
        except Exception as e:
            import traceback
            error_traceback = traceback.format_exc()
            logger.error("处理过程中发生错误", {
                "error": str(e),
                "traceback": error_traceback
            })
            print(f"\n错误详情: {str(e)}")
            print(error_traceback)


if __name__ == "__main__":
    demonstrate_schema_parsing()
