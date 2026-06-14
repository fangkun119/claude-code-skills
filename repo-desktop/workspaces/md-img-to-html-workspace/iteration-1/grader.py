#!/usr/bin/env python3
"""
评估脚本：检查 md-img-to-html skill 的转换结果
"""
import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Any

def check_markdown_images(content: str) -> int:
    """检查是否还有 Markdown 图片语法"""
    # Wikilink 格式
    wikilink_pattern = r'!\[\[([^\]]+)\]\]'
    wikilink_matches = re.findall(wikilink_pattern, content)

    # 标准 Markdown 格式
    standard_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    standard_matches = re.findall(standard_pattern, content)

    return len(wikilink_matches) + len(standard_matches)

def check_html_img_consistency(content: str) -> int:
    """检查 HTML img 标签是否包含必要的 style 属性"""
    # 匹配 <img> 标签
    img_pattern = r'<img\s+[^>]*style="([^"]*)"[^>]*>'
    img_matches = re.findall(img_pattern, content)

    # 每个 style 应该包含 display: block
    consistent = sum(1 for style in img_matches if 'display: block' in style and 'width:' in style)
    return consistent

def check_width_preservation(content: str) -> Dict[str, int]:
    """检查宽度参数是否正确保留"""
    img_pattern = r'<img\s+[^>]*style="[^"]*width:\s*([^;]+);[^"]*"[^>]*alt="([^"]*)"[^>]*>'
    matches = re.findall(img_pattern, content)

    widths = {}
    for width, alt in matches:
        if width not in widths:
            widths[width] = 0
        widths[width] += 1

    return widths

def check_alt_preservation(content: str) -> int:
    """检查 alt 文本是否正确保留"""
    # 检查所有 img 标签是否有 alt 属性
    img_pattern = r'<img\s+[^>]*alt="([^"]*)"[^>]*>'
    matches = re.findall(img_pattern, content)
    return len(matches)

def check_regular_links(content: str) -> int:
    """检查普通 Markdown 链接是否被保留"""
    # 普通链接格式 [text](url)
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    # 排除图片链接
    non_img_links = [m for m in re.findall(link_pattern, content) if not m[0].startswith('!')]
    return len(non_img_links)

def check_existing_html_preserved(original_content: str, converted_content: str) -> bool:
    """检查已存在的 HTML img 标签是否被保留"""
    # 提取原始内容中的 HTML img 标签
    original_imgs = re.findall(r'<img\s+[^>]*>', original_content)
    # 检查这些标签是否仍在转换后的内容中
    preserved = sum(1 for img in original_imgs if img in converted_content)
    return preserved == len(original_imgs) if original_imgs else True

def grade_eval(eval_dir: Path) -> Dict[str, Any]:
    """评估单个测试用例"""
    metadata_path = eval_dir / "eval_metadata.json"
    with_skill_dir = eval_dir / "with_skill" / "outputs"
    without_skill_dir = eval_dir / "without_skill" / "outputs"

    # 读取元数据
    with open(metadata_path) as f:
        metadata = json.load(f)

    # 找到输出文件
    with_skill_files = list(with_skill_dir.glob("*.md"))
    without_skill_files = list(without_skill_dir.glob("*.md"))

    results = {
        "eval_name": metadata["eval_name"],
        "assertions": []
    }

    for config_name, output_files in [("with_skill", with_skill_files), ("without_skill", without_skill_files)]:
        if not output_files:
            continue

        output_file = output_files[0]
        with open(output_file) as f:
            content = f.read()

        config_results = {
            "config": config_name,
            "assertion_results": []
        }

        for assertion in metadata["assertions"]:
            result = {
                "name": assertion["name"],
                "passed": False,
                "evidence": ""
            }

            if assertion["name"] == "转换所有Markdown图片" or assertion["name"] == "转换所有wikilink图片" or assertion["name"] == "转换标准Markdown图片" or assertion["name"] == "所有图片都被转换":
                remaining = check_markdown_images(content)
                result["passed"] = remaining == 0
                result["evidence"] = f"发现 {remaining} 个未转换的 Markdown 图片"

            elif assertion["name"] == "保持HTML格式一致性":
                consistent = check_html_img_consistency(content)
                total_imgs = len(re.findall(r'<img[^>]*>', content))
                result["passed"] = consistent == total_imgs
                result["evidence"] = f"{consistent}/{total_imgs} 个 img 标签包含正确的 style 属性"

            elif assertion["name"] == "保留宽度参数" or assertion["name"] == "保留指定宽度":
                widths = check_width_preservation(content)
                # 检查是否有具体的宽度值
                has_specific_width = any(w != '100%' for w in widths.keys())
                result["passed"] = has_specific_width or '100%' in widths
                result["evidence"] = f"发现的宽度值: {list(widths.keys())}"

            elif assertion["name"] == "保留alt文本" or assertion["name"] == "wikilink的alt为空" or assertion["name"] == "处理空alt文本":
                alt_count = check_alt_preservation(content)
                total_imgs = len(re.findall(r'<img[^>]*>', content))
                result["passed"] = alt_count == total_imgs
                result["evidence"] = f"{alt_count}/{total_imgs} 个 img 标签有 alt 属性"

            elif assertion["name"] == "默认宽度为100%":
                widths = check_width_preservation(content)
                result["passed"] = '100%' in widths
                result["evidence"] = f"宽度值: {list(widths.keys())}"

            elif assertion["name"] == "不修改普通链接" or assertion["name"] == "不转换普通链接":
                links = check_regular_links(content)
                result["passed"] = links > 0
                result["evidence"] = f"发现 {links} 个普通链接被保留"

            elif assertion["name"] == "不重复处理HTML标签" or assertion["name"] == "不重复处理HTML":
                # 简单检查：不应该有双重转换的痕迹
                no_double_img = '<img<img' not in content and '<img><img' not in content
                result["passed"] = no_double_img
                result["evidence"] = "检查是否有双重 img 标签"

            elif assertion["name"] == "从下到上处理":
                # 检查所有图片都被转换（没有遗漏）
                remaining = check_markdown_images(content)
                result["passed"] = remaining == 0
                result["evidence"] = f"所有图片都被转换，没有遗漏"

            config_results["assertion_results"].append(result)

        results["assertions"].append(config_results)

    return results

def main():
    """主函数"""
    iteration_dir = Path(__file__).parent

    results = []
    for eval_dir in sorted(iteration_dir.glob("eval-*")):
        if eval_dir.is_dir():
            eval_result = grade_eval(eval_dir)
            results.append(eval_result)

    # 保存评分结果
    grading_file = iteration_dir / "grading.json"
    with open(grading_file, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"评分完成，结果保存到: {grading_file}")

    # 打印摘要
    for eval_result in results:
        print(f"\n## {eval_result['eval_name']}")
        for config_result in eval_result["assertions"]:
            config_name = config_result["config"]
            passed = sum(1 for a in config_result["assertion_results"] if a["passed"])
            total = len(config_result["assertion_results"])
            print(f"  {config_name}: {passed}/{total} 断言通过")

if __name__ == "__main__":
    main()
