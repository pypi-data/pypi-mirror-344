'''
Description:  
Author: Huang J
Date: 2025-04-28 09:14:00
'''

import re
from typing import List

def segmentchunker(
    text: str,
    language: str,
    seg_size: int = 200,
    seg_overlap: int = 1,
    separators: List[str] = None
) -> List[str]:
    """
    段落分块，支持设置分隔符和重叠段落数量
    
    参数：
    text: 要分割的原始文本
    language: 语言类型 ('zh'/'en')
    seg_size: 目标块大小（字符数）
    seg_overlap: 块间重叠的块数，不是字符数
    separators: 自定义分隔符列表
    
    返回：
    List[str]: 分割后的文本块列表
    """

    if seg_size <= 0:
        raise ValueError("seg_size 必须大于0")
    if seg_overlap < 0:
        raise ValueError("seg_overlap 不能为负数")

    lang_config = {
        'zh': ['\n\n', '\n', '。', '！', '？', '；', '，', '、'],
        'en': ['\n\n', '\n', '.', '!', '?', ';', ',']
    }
    separators = separators or lang_config.get(language, [])
    
    split_segs = []
    if separators:
        separators_sorted = sorted(separators, key=lambda x: (-len(x), x))
        pattern = re.compile(r'(' + r'|'.join(map(re.escape, separators_sorted)) + r')')
        parts = pattern.split(text)
        
        merged = []
        for i in range(0, len(parts), 2):
            segment = parts[i].strip()
            if i+1 < len(parts):
                segment += parts[i+1].strip() 
            if segment:
                merged.append(segment)
        split_segs = merged
    else:
        if text.strip():
            split_segs = [text.strip()]

    chunks = []
    n = len(split_segs)
    i = 0
    
    while i < n:
        start_idx = i
        current_chunk = []
        current_len = 0
        
        while i < n and current_len + len(split_segs[i]) <= seg_size:
            current_chunk.append(split_segs[i])
            current_len += len(split_segs[i])
            i += 1
        
        if (remaining := sum(len(s) for s in split_segs[i:])) > 0:
            if 0 < remaining < seg_size and (current_len + remaining) <= seg_size:
                current_chunk.extend(split_segs[i:])
                i = n
        
        if current_chunk:
            chunks.append(''.join(current_chunk))
            if seg_overlap > 0 and i < n:
                effective_overlap = min(seg_overlap, len(current_chunk))                
                i = max(start_idx + len(current_chunk) - effective_overlap, start_idx + 1)

    return chunks
                
            
    
    
    
    
    
    
    
    
