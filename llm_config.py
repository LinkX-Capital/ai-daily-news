#!/usr/bin/env python3
"""大模型接口配置 - 所有 LLM 调用统一从这里取地址、key 和模型名

默认走 MiniMax（Anthropic 兼容接口）。换成其他 Anthropic 兼容服务时只改 .env：
  LLM_API_URL      接口地址，例如 https://api.deepseek.com/anthropic/v1/messages
  LLM_API_KEY      对应服务的 key；未设置时回退到 MINIMAX_API_KEY
  LLM_MODEL_MAIN   主力模型（选稿 + 中文写作）
  LLM_MODEL_LIGHT  轻量模型（QA、补充、翻译、推文摘要）；未设置时各脚本用原来的 MiniMax 型号
  LLM_LIGHT_THINKING=disabled  轻量任务关闭 thinking（DeepSeek 需要）
"""

import os

API_URL = os.environ.get("LLM_API_URL", "https://api.minimaxi.com/anthropic/v1/messages")
API_KEY = os.environ.get("LLM_API_KEY") or os.environ.get("MINIMAX_API_KEY", "")
MODEL_MAIN = os.environ.get("LLM_MODEL_MAIN", "MiniMax-M3")


def light_model(minimax_default):
    """轻量任务的模型名；未配置 LLM_MODEL_LIGHT 时保留调用方原来的 MiniMax 型号"""
    return os.environ.get("LLM_MODEL_LIGHT") or minimax_default


def light_extra():
    """轻量任务的附加请求参数。

    DeepSeek 默认先输出 thinking，会吃掉 QA/标题/重点提取这类小 max_tokens 调用的预算，
    导致正文被截断；设 LLM_LIGHT_THINKING=disabled 时关闭。MiniMax 默认不受影响。
    """
    if os.environ.get("LLM_LIGHT_THINKING", "").lower() == "disabled":
        return {"thinking": {"type": "disabled"}}
    return {}


def llm_headers(api_key=None):
    """Anthropic 兼容接口请求头；同时带 Bearer 和 x-api-key，兼容 MiniMax 与 DeepSeek"""
    key = api_key or API_KEY
    return {
        "Authorization": f"Bearer {key}",
        "x-api-key": key,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
    }
