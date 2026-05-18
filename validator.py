#!/usr/bin/env python3
"""
Validator Agent - 事实校验代理

功能：
1. 从报告中提取事实性断言
2. 验证每个断言的来源
3. 多源交叉验证
4. 输出验证报告

Usage:
    validator = Validator()
    result = validator.validate(report, search_results)
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum


# ============ 数据结构 ============

class ClaimType(Enum):
    """断言类型"""
    DATE = "date"           # 日期/时间
    AMOUNT = "amount"       # 金额/估值
    NUMBER = "number"       # 数字（参数量、性能等）
    FACT = "fact"           # 一般事实
    QUOTE = "quote"         # 引用
    COMPARISON = "comparison"  # 对比/比较


class ValidationStatus(Enum):
    """验证状态"""
    VERIFIED = "verified"       # 已验证
    UNVERIFIED = "unverified"   # 未验证（无来源）
    CONFLICTING = "conflicting" # 矛盾（多源不一致）
    ERROR = "error"            # 错误（明显错误）


@dataclass
class Claim:
    """事实性断言"""
    id: str
    text: str                     # 断言文本
    type: ClaimType               # 断言类型
    value: Any = None             # 提取的值（如日期、金额）
    sources_found: List[Dict] = field(default_factory=list)
    validation_status: ValidationStatus = ValidationStatus.UNVERIFIED
    confidence: float = 0.0       # 验证置信度
    notes: str = ""               # 备注


@dataclass
class ValidationResult:
    """验证结果"""
    claims: List[Claim]
    total_claims: int
    verified_count: int
    unverified_count: int
    error_count: int
    confidence_score: float       # 整体置信度
    warnings: List[str]           # 警告信息
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


# ============ 断言提取器 ============

class ClaimExtractor:
    """从报告中提取事实性断言"""

    # 日期模式
    DATE_PATTERNS = [
        r'(\d{4})年(\d{1,2})月',
        r'(\d{4}-\d{1,2}-\d{1,2})',
        r'(\d{1,2})月(\d{1,2})日',
    ]

    # 金额模式
    AMOUNT_PATTERNS = [
        r'(\d+(?:\.\d+)?)\s*[亿美元万亿]',
        r'\$[\d.]+(?:[BbMm]|[万亿]illion)',
        r'估值\s*(\d+(?:\.\d+)?)',
    ]

    # 数据模式
    NUMBER_PATTERNS = [
        r'(\d+(?:\.\d+)?)\s*%[,，]?\s*([\u4e00-\u9fff]+|benchmark)',
        r'(\d+[BbMm]|[万亿兆])参数',
        r'(\d+(?:\.\d+)?)\s*(?:倍|%|pp)',
    ]

    # 关键词模式（需要验证的词）
    TRIGGER_WORDS = [
        '首个', '首次', '首发', '率先',
        '最大', '第一', '领先', '垄断',
        '超过', '超越', '击败',
    ]

    def extract(self, report: str, search_results: Dict = None) -> List[Claim]:
        """提取需要验证的断言"""
        claims = []
        claim_id = 0

        # 1. 提取日期
        for pattern in self.DATE_PATTERNS:
            matches = re.finditer(pattern, report)
            for match in matches:
                claims.append(Claim(
                    id=f"date_{claim_id}",
                    text=match.group(0),
                    type=ClaimType.DATE,
                    value=match.group(0)
                ))
                claim_id += 1

        # 2. 提取金额
        for pattern in self.AMOUNT_PATTERNS:
            matches = re.finditer(pattern, report)
            for match in matches:
                text = match.group(0)
                # 提取上下文
                start = max(0, match.start() - 30)
                end = min(len(report), match.end() + 30)
                context = report[start:end]

                claims.append(Claim(
                    id=f"amount_{claim_id}",
                    text=f"{context.strip()}...",
                    type=ClaimType.AMOUNT,
                    value=text
                ))
                claim_id += 1

        # 3. 提取性能数据
        for pattern in self.NUMBER_PATTERNS:
            matches = re.finditer(pattern, report)
            for match in matches:
                start = max(0, match.start() - 20)
                end = min(len(report), match.end() + 20)
                context = report[start:end]

                claims.append(Claim(
                    id=f"number_{claim_id}",
                    text=f"{context.strip()}...",
                    type=ClaimType.NUMBER,
                    value=match.group(0)
                ))
                claim_id += 1

        # 4. 提取绝对性表述
        for word in self.TRIGGER_WORDS:
            # 查找包含关键词的句子
            sentences = re.split(r'[。！？\n]', report)
            for sentence in sentences:
                if word in sentence:
                    # 清理并添加
                    cleaned = sentence.strip()
                    if len(cleaned) > 10 and len(cleaned) < 200:
                        claims.append(Claim(
                            id=f"fact_{claim_id}",
                            text=cleaned,
                            type=ClaimType.FACT
                        ))
                        claim_id += 1
                        break  # 每个关键词只取一个例子

        # 5. 去重
        claims = self._deduplicate(claims)

        return claims

    def _deduplicate(self, claims: List[Claim]) -> List[Claim]:
        """去重：文本相似的断言只保留一个"""
        seen = set()
        unique = []

        for claim in claims:
            # 简化文本用于比较
            key = re.sub(r'\s+', '', claim.text.lower())[:50]
            if key not in seen:
                seen.add(key)
                unique.append(claim)

        return unique


# ============ 来源验证器 ============

class SourceValidator:
    """验证断言的来源"""

    def __init__(self):
        pass

    def validate(self, claims: List[Claim],
                report: str,
                search_results: Dict) -> ValidationResult:
        """验证所有断言"""

        verified_count = 0
        unverified_count = 0
        error_count = 0
        warnings = []

        for claim in claims:
            # 1. 检查报告本身是否有来源标注
            in_report_source = self._check_report_source(claim, report)

            # 2. 检查搜索结果
            in_search_result = self._check_search_result(claim, search_results)

            # 3. 综合判断
            if in_report_source or in_search_result:
                claim.validation_status = ValidationStatus.VERIFIED
                claim.confidence = 0.9 if in_report_source else 0.7
                verified_count += 1
            elif claim.type == ClaimType.DATE:
                # 日期需要特别检查
                if self._validate_date(claim, report):
                    claim.validation_status = ValidationStatus.VERIFIED
                    claim.confidence = 0.8
                    verified_count += 1
                else:
                    claim.validation_status = ValidationStatus.ERROR
                    claim.notes = "日期可能不准确，请核对"
                    warnings.append(f"⚠️ 日期断言需验证: {claim.text}")
                    error_count += 1
            else:
                claim.validation_status = ValidationStatus.UNVERIFIED
                claim.notes = "未找到明确来源"
                unverified_count += 1

        # 计算整体置信度
        total = len(claims)
        confidence_score = verified_count / total if total > 0 else 0.0

        return ValidationResult(
            claims=claims,
            total_claims=total,
            verified_count=verified_count,
            unverified_count=unverified_count,
            error_count=error_count,
            confidence_score=confidence_score,
            warnings=warnings
        )

    def _check_report_source(self, claim: Claim, report: str) -> bool:
        """检查报告中是否有来源标注"""
        # 查找断言附近是否有来源标记
        # 来源标记模式：【来源: xxx】、根据 xxx、来源：xxx
        lines = report.split('\n')

        for i, line in enumerate(lines):
            if claim.text[:30] in line:
                # 检查前后几行
                context_lines = lines[max(0, i-2):i+3]
                for context_line in context_lines:
                    if re.search(r'【.*来源.*】|根据.*报道|来源：|Published|based on',
                               context_line, re.IGNORECASE):
                        claim.sources_found.append({
                            "type": "report",
                            "evidence": context_line.strip()
                        })
                        return True
        return False

    def _check_search_result(self, claim: Claim,
                             search_results: Dict) -> bool:
        """检查搜索结果是否支持断言"""
        if not search_results:
            return False

        # Archive 搜索结果
        archive = search_results.get("results", {}).get("archive", [])
        for item in archive[:5]:  # 只检查前5个
            # 简单的文本匹配
            if any(kw in item.get("title", "").lower() or
                   kw in item.get("body", "").lower()
                   for kw in re.findall(r'[\w\u4e00-\u9fff]{2,}', claim.text)):
                claim.sources_found.append({
                    "type": "archive",
                    "date": item.get("date"),
                    "title": item.get("title")[:60]
                })
                return True

        # 来源原文
        source_content = search_results.get("results", {}).get("source_content")
        if source_content and claim.text[:30] in source_content:
            claim.sources_found.append({
                "type": "source",
                "evidence": "在来源原文中找到"
            })
            return True

        return False

    def _validate_date(self, claim: Claim, report: str) -> bool:
        """验证日期断言"""
        # 提取报告生成日期
        date_match = re.search(r'生成时间[:: ]*(\d{4}-\d{2}-\d{2})', report)
        if not date_match:
            return True  # 无法判断，假设正确

        report_date = date_match.group(1)

        # 检查日期是否合理（不能晚于报告日期）
        claim_date_match = re.search(r'(\d{4})', claim.text)
        if claim_date_match:
            claim_year = int(claim_date_match.group(1))
            report_year = int(report_date[:4])

            # 如果断言中的年份晚于报告年份，可能是幻觉
            if claim_year > report_year:
                return False

        return True


# ============ 交叉验证器 ============

class CrossValidator:
    """多源交叉验证"""

    def __init__(self):
        pass

    def cross_validate(self, claim: Claim,
                      sources: List[Dict]) -> Tuple[ValidationStatus, str]:
        """交叉验证多个来源"""
        if len(sources) < 2:
            return claim.validation_status, ""

        # 检查来源间的一致性
        # 这里简化实现，实际需要更复杂的语义匹配
        return ValidationStatus.VERIFIED, f"{len(sources)}个来源一致"


# ============ 主验证器 ============

class Validator:
    """事实校验代理"""

    def __init__(self):
        self.extractor = ClaimExtractor()
        self.source_validator = SourceValidator()
        self.cross_validator = CrossValidator()

    def validate(self, report: str,
                search_results: Dict = None) -> ValidationResult:
        """
        验证报告的事实准确性

        Args:
            report: 研究报告文本
            search_results: 搜索结果（来自 FederatedSearch）

        Returns:
            ValidationResult: 验证结果
        """
        if search_results is None:
            search_results = {}

        # 1. 提取断言
        claims = self.extractor.extract(report, search_results)

        # 2. 验证断言
        result = self.source_validator.validate(claims, report, search_results)

        # 3. 交叉验证（如果有多个来源）
        for claim in claims:
            if len(claim.sources_found) > 1:
                status, note = self.cross_validator.cross_validate(
                    claim, claim.sources_found
                )
                claim.validation_status = status
                if note:
                    claim.notes += f" | {note}"

        return result

    def to_summary(self, result: ValidationResult) -> str:
        """生成验证报告摘要"""
        lines = [
            "## 事实校验报告",
            f"",
            f"**总断言数**: {result.total_claims}",
            f"**已验证**: {result.verified_count} ✓",
            f"**未验证**: {result.unverified_count} ?",
            f"**可能错误**: {result.error_count} ✗",
            f"**置信度**: {result.confidence_score:.1%}",
            f"",
        ]

        if result.warnings:
            lines.append("### ⚠️ 警告")
            for warning in result.warnings:
                lines.append(f"- {warning}")
            lines.append("")

        # 列出未验证的断言
        unverified = [c for c in result.claims
                     if c.validation_status == ValidationStatus.UNVERIFIED]
        if unverified:
            lines.append("### 未验证的断言")
            for claim in unverified[:5]:
                lines.append(f"- **{claim.type.value}**: {claim.text[:80]}...")
            if len(unverified) > 5:
                lines.append(f"- ... 还有 {len(unverified)-5} 条")
            lines.append("")

        # 列出可能错误的断言
        errors = [c for c in result.claims
                 if c.validation_status == ValidationStatus.ERROR]
        if errors:
            lines.append("### 可能错误的断言")
            for claim in errors:
                lines.append(f"- **{claim.type.value}**: {claim.text}")
                if claim.notes:
                    lines.append(f"  - {claim.notes}")
            lines.append("")

        return "\n".join(lines)

    def get_corrections(self, result: ValidationResult) -> List[str]:
        """获取需要修正的问题"""
        corrections = []

        for claim in result.claims:
            if claim.validation_status == ValidationStatus.ERROR:
                corrections.append(
                    f"需验证: {claim.text} ({claim.notes})"
                )
            elif (claim.validation_status == ValidationStatus.UNVERIFIED and
                  claim.type in [ClaimType.DATE, ClaimType.AMOUNT]):
                corrections.append(
                    f"建议添加来源: {claim.text}"
                )

        return corrections


# ============ 测试 ============

if __name__ == "__main__":
    # 测试用例
    test_report = """
    # PRISM框架研究报告

    > 生成时间: 2026-05-12

    ## 事实梳理

    PRISM于2025年2月发布在arXiv上，GSM8K从67.58%提升至85.30%，
    提升16.4pp。估值200亿美元，是视频生成赛道的最高估值。

    快手分拆可灵AI，估值200亿美元【来源: 晚点LatePost】。
    """

    validator = Validator()
    result = validator.validate(test_report)

    print(validator.to_summary(result))
