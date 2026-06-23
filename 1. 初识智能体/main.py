"""1.3 动手体验:从零实现一个智能体"""

from tavily.tavily import TavilyClient

import requests
from config import Config


AGENT_SYSTEM_PROMPT = """
你是一名智能旅行助手，你的任务的分析用户请求，并使用可用工具一步一步解决问题

# 可用工具
- `get_weather(city: str)`: 查询指定城市天气
- `get_attraction(city: str , weather: str)` : 根据城市和天气推荐景点

# 输出格式
你的输出每次必须严格按照一下格式，包含一对Thought和ACTION

- Thought : [你思考的过程]
- ACTION : [你要执行的动作]

ACTION的格式必须是以下之一
1. 调用工具 : function_name(arg_name: "arg_value")
2. 结束任务 : Finish[最终答案]

# 重要提示：
- 每次只输出一对 Thought-ACTION
- ACTION必须在同一行不要换行
- 当收集到的信息足够回答问题的时候，你必须使用ACTION : Thought[最终回答] 的格式结束
"""


def get_weather(city: str) -> str:
    try:
        # Request weather info
        r = requests.get("https://wttr.in/{city}?format=j2")
        # Check request status to be 200
        r.raise_for_status()
        # Get data
        data = r.json()
        current_condition = data["current_condition"][0]
        temperature = current_condition["temp_C"]
        weatherDesc = current_condition["weatherDesc"][0]["value"]
        responce = f"{city}当前气温{temperature}摄氏度,天气状况：{weatherDesc}"

        return responce

    except requests.exceptions.RequestException:
        return "Network error , unable to access target website - {e}"

    except (KeyError, IndexError) as e:
        return (
            f"Error parsing data. possibly because the target city does not exist - {e}"
        )


def get_attraction(city: str, weather: str) -> str:
    api_key = Config.TAVILY_API_KEY
    if not api_key:
        return "TAVILY_API_KEY is not set"
    try:
        tavily = TavilyClient(api_key=api_key)
        r = tavily.search(f"{city}在{weather}天气下最值得去的景点推荐和介绍")
        if r.get("answer"):
            return r["answer"]

        # If answer is None , format result manual
        formate_list = []
        for result in r["results"]:
            formate_list.append(f"- {result['title']}:{result['content']}")
        if not formate_list:
            return "抱歉没有找到推荐的景点"
        return "根据搜索，为您找到以下信息:\n" + "\n".join(formate_list)

    except Exception as e:
        return f"Error calling tavily server! -{e}"
