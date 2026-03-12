#!/usr/bin/env python3
"""配置加载器 - 统一管理外部配置"""

import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
_config = None

def load_config():
    """加载配置文件"""
    global _config
    if _config is None:
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                _config = json.load(f)
        except FileNotFoundError:
            print(f"⚠️ 配置文件不存在: {CONFIG_FILE}")
            _config = {}
        except json.JSONDecodeError as e:
            print(f"⚠️ 配置文件格式错误: {e}")
            _config = {}
    return _config

def get(path, default=None):
    """获取配置项，支持路径访问
    
    Examples:
        get("twitter.company_accounts") -> [...]
        get("research.subfields.LLM/大语言模型.keywords") -> [...]
    """
    config = load_config()
    keys = path.split(".")
    value = config
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default
    return value

# 便捷访问函数
def twitter_company_accounts():
    return set(get("twitter.company_accounts", []))

def twitter_researcher_accounts():
    return set(get("twitter.researcher_accounts", []))

def tier1_ai_companies():
    return get("companies.tier1_ai_companies", [])

def research_subfields():
    return get("research.subfields", {})

def top_conferences():
    return get("research.conferences", {})

def high_citation_authors():
    return get("research.high_citation_authors", {})

def official_sources():
    return get("companies.official_sources", {})

def compute_keywords():
    return get("classification.compute_keywords", [])

def capex_keywords():
    return get("classification.capex_keywords", [])

def research_keywords():
    return get("classification.research_keywords", [])

def funding_keywords():
    return get("classification.funding_keywords", [])

def model_keywords():
    return get("classification.model_keywords", [])

def non_news_keywords():
    return get("filter.non_news_keywords", [])

if __name__ == "__main__":
    # 测试配置加载
    print("📦 配置加载测试")
    print(f"  公司账号: {len(twitter_company_accounts())} 个")
    print(f"  研究者账号: {len(twitter_researcher_accounts())} 个")
    print(f"  研究领域: {len(research_subfields())} 个")
    print(f"  算力关键词: {len(compute_keywords())} 个")
    print(f"  过滤关键词: {len(non_news_keywords())} 个")
