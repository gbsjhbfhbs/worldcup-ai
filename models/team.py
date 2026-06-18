"""球队数据模型 — 不可变 dataclass"""
from dataclasses import dataclass, field
from typing import Tuple, List


@dataclass(frozen=True)
class Player:
    """球员信息（不可变）"""
    name: str
    position: str           # GK/DF/MF/FW
    club: str = ""
    caps: int = 0           # 国家队出场
    goals: int = 0          # 国家队进球
    age: int = 0


@dataclass(frozen=True)
class Team:
    """球队完整信息（不可变）"""
    code: str                       # FIFA 三字母代码 "FRA"
    name: str                       # 中文名 "法国"
    name_en: str                    # 英文名 "France"
    fifa_rank: int
    elo_rating: float
    confederation: str              # UEFA/CONMEBOL/...
    group: str                      # 小组 "A"~"L"
    coach: str = ""
    key_players: Tuple[str, ...] = ()
    recent_form: Tuple[str, ...] = ()   # 近5场 ["W","D","L"...]
    avg_goals: float = 0.0
    avg_conceded: float = 0.0
    world_cup_titles: int = 0
    squad: Tuple[Player, ...] = ()
    flag_path: str = ""             # 国旗图片相对路径

    @classmethod
    def from_dict(cls, code: str, data: dict) -> "Team":
        """从字典创建 Team 实例（输入校验 + 不可变转换）"""
        players = tuple(
            Player(**p) for p in data.get("squad", [])
        )
        return cls(
            code=code,
            name=data.get("name", code),
            name_en=data.get("name_en", code),
            fifa_rank=data.get("fifa_rank", 999),
            elo_rating=data.get("elo_rating", 1500.0),
            confederation=data.get("confederation", ""),
            group=data.get("group", ""),
            coach=data.get("coach", ""),
            key_players=tuple(data.get("key_players", [])),
            recent_form=tuple(data.get("recent_form", [])),
            avg_goals=data.get("avg_goals", 0.0),
            avg_conceded=data.get("avg_conceded", 0.0),
            world_cup_titles=data.get("world_cup_titles", 0),
            squad=players,
            flag_path=data.get("flag_path", ""),
        )
