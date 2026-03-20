#!/usr/bin/env python3
"""使用playwright生成手机端长图"""

import asyncio
from playwright.async_api import async_playwright
import os

async def generate_screenshot():
    html_file = "/Users/shenyalan/ai-daily-news/daily-ai-news.html"

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": 375, "height": 1200},  # 手机端宽度
            device_scale_factor=2  # 2x清晰度
        )

        # 读取HTML内容
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        await page.set_content(html_content)

        # 等待渲染完成
        await page.wait_for_timeout(2000)

        # 获取完整页面高度
        height = await page.evaluate("document.body.scrollHeight")

        # 设置 viewport 为完整高度
        await page.set_viewport_size({"width": 375, "height": height})

        # 截图
        output_file = "/Users/shenyalan/ai-daily-news/daily-ai-news-mobile.png"
        await page.screenshot(path=output_file, full_page=True)

        await browser.close()
        print(f"✅ 已生成手机端长图: {output_file}")

if __name__ == "__main__":
    asyncio.run(generate_screenshot())
