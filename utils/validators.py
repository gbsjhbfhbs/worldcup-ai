"""输入校验 — 集中管理所有校验逻辑"""
import re
from typing import Tuple, Optional


# match_id 格式: G-[A-L]-[1-6] (小组赛) 或 KO-{R32,R16,QF,SF,3RD,F}-[0-9]+ (淘汰赛)
MATCH_ID_PATTERN = re.compile(
    r'^(G-[A-L]-[1-6]|KO-(R32|R16|QF|SF|3RD|F)-\d+)$'
)


def validate_match_id(match_id: str) -> bool:
    """校验 match_id 格式"""
    return bool(MATCH_ID_PATTERN.match(match_id)) if match_id else False


def validate_probabilities(home: int, draw: int, away: int) -> bool:
    """校验三个概率值：和为 100，每个在 0-100 范围"""
    if not all(isinstance(x, int) for x in (home, draw, away)):
        return False
    if not all(0 <= x <= 100 for x in (home, draw, away)):
        return False
    return (home + draw + away) == 100


def parse_score(score_str: str) -> Optional[Tuple[int, int]]:
    """解析比分字符串 "2-1" -> (2, 1)"""
    score_str = score_str.strip()
    match = re.match(r'^(\d{1,2})\s*-\s*(\d{1,2})$', score_str)
    if not match:
        return None
    h, a = int(match.group(1)), int(match.group(2))
    if h < 0 or a < 0 or h > 20 or a > 20:
        return None
    return (h, a)


def validate_team_code(code: str, valid_codes: set) -> bool:
    """校验球队三字母代码"""
    return code.upper() in valid_codes if code and valid_codes else True
