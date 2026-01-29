"""
判断成绩是否及格。

规则：60分及格
"""


def is_pass(score: int) -> bool:
    """判断 score 是否及格。"""
    if score > 60:
        return True
    return False
