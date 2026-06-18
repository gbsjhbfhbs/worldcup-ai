"""JSON 数据加载与校验"""
import json
from pathlib import Path
from typing import Dict, List, Optional
from functools import lru_cache

from config import Config
from models.match import Match, MatchStage
from models.team import Team


class DataLoader:
    """加载 data/ 下的 JSON 文件，提供查询接口"""

    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or Config.DATA_DIR
        self._teams: Dict[str, Team] = {}
        self._matches: List[Match] = []
        self._groups: Dict[str, list] = {}
        self._head_to_head: Dict[str, dict] = {}
        self._loaded = False

    def load_all(self) -> None:
        """加载所有数据文件"""
        if self._loaded:
            return
        self._load_teams()
        self._load_schedule()
        self._load_groups()
        self._load_head_to_head()
        self._loaded = True

    def _load_teams(self) -> None:
        path = self.data_dir / "teams.json"
        if not path.exists():
            raise FileNotFoundError(f"球队数据文件不存在: {path}")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for code, d in data.items():
            self._teams[code] = Team.from_dict(code, d)

    def _load_schedule(self) -> None:
        path = self.data_dir / "schedule.json"
        if not path.exists():
            return
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        from datetime import datetime
        for m in data.get("matches", []):
            stage_map = {
                "group": MatchStage.GROUP,
                "round_of_32": MatchStage.ROUND_OF_32,
                "round_of_16": MatchStage.ROUND_OF_16,
                "quarter_final": MatchStage.QUARTER_FINAL,
                "semi_final": MatchStage.SEMI_FINAL,
                "third_place": MatchStage.THIRD_PLACE,
                "final": MatchStage.FINAL,
            }
            match_date = None
            if m.get("match_date"):
                try:
                    match_date = datetime.fromisoformat(m["match_date"])
                except (ValueError, TypeError):
                    pass
            self._matches.append(Match(
                match_id=m["match_id"],
                home_team=m["home_team"],
                away_team=m["away_team"],
                stage=stage_map.get(m.get("stage", "group"), MatchStage.GROUP),
                group=m.get("group"),
                match_date=match_date,
                stadium=m.get("stadium", ""),
                city=m.get("city", ""),
                home_score=m.get("home_score"),
                away_score=m.get("away_score"),
            ))

    def _load_groups(self) -> None:
        path = self.data_dir / "groups.json"
        if not path.exists():
            return
        with open(path, "r", encoding="utf-8") as f:
            self._groups = json.load(f)

    def _load_head_to_head(self) -> None:
        path = self.data_dir / "historical" / "head_to_head.json"
        if not path.exists():
            return
        with open(path, "r", encoding="utf-8") as f:
            self._head_to_head = json.load(f)

    # ---- 查询接口 ----

    def get_team(self, code: str) -> Optional[Team]:
        return self._teams.get(code.upper())

    def get_all_teams(self) -> Dict[str, Team]:
        return dict(self._teams)

    def get_teams_by_group(self, group: str) -> List[Team]:
        return [t for t in self._teams.values() if t.group == group]

    @lru_cache(maxsize=128)
    def get_match(self, match_id: str) -> Optional[Match]:
        for m in self._matches:
            if m.match_id == match_id:
                return m
        return None

    def get_all_matches(self) -> List[Match]:
        return list(self._matches)

    def get_matches_by_date(self, date_str: str) -> List[Match]:
        """按日期筛选比赛，date_str 格式 '2026-06-11'"""
        result = []
        for m in self._matches:
            if m.match_date and m.match_date.strftime("%Y-%m-%d") == date_str:
                result.append(m)
        return result

    def get_upcoming_matches(self, limit: int = 10) -> List[Match]:
        """获取即将进行的比赛"""
        from datetime import datetime
        now = datetime.now()
        upcoming = [m for m in self._matches
                    if not m.is_played() and m.match_date and m.match_date > now]
        upcoming.sort(key=lambda m: m.match_date)
        return upcoming[:limit]

    def get_played_matches(self) -> List[Match]:
        """获取已结束的比赛"""
        return [m for m in self._matches if m.is_played()]

    def get_group_teams(self, group: str) -> List[str]:
        """获取某小组的球队代码列表"""
        return self._groups.get(group, [])

    def get_group_label(self, group: str) -> str:
        """获取小组的中文显示标签，如 'A组 · 墨西哥/韩国/南非/捷克'"""
        teams = self._groups.get(group, [])
        names = []
        for code in teams:
            team = self._teams.get(code)
            names.append(team.name if team else code)
        return f"{group}组 · {' / '.join(names)}"

    def get_all_group_labels(self) -> dict:
        """获取所有小组的中文标签 {group: label}"""
        return {g: self.get_group_label(g) for g in sorted(self._groups.keys())}

    def get_head_to_head(self, team1: str, team2: str) -> Optional[str]:
        """获取两队历史交锋记录（格式化文本）"""
        key1 = f"{team1}_{team2}"
        key2 = f"{team2}_{team1}"
        record = self._head_to_head.get(key1) or self._head_to_head.get(key2)
        if not record:
            return None
        # 格式化为文本
        return (f"近 {record['total']} 次交手："
                f"{team1} {record['wins_team1']} 胜 "
                f"{record['draws']} 平 "
                f"{team2} {record['wins_team2']} 胜")
