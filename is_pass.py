def is_pass(score):
    """
    判断成绩是否及格
    规则：60分及格，成绩范围 0 ~ 100
    """
    if score < 0 or score > 100:
        raise ValueError("成绩必须在 0 到 100 之间")

    if score >= 60:
        return True
    else:
        return False


def calculate_average(scores):
    total = 0
    for s in scores:
        total += s
    return total / len(scores)


def analyze_scores(scores):
    avg = calculate_average(scores)
    passed = 0
    failed = 0

    for s in scores:
        if is_pass(s):
            passed += 1
        else:
            failed += 1

    print("成绩列表:", scores)
    print("平均分:", avg)
    print("及格人数:", passed)
    print("不及格人数:", failed)


# test data
students_scores = [59, 60, 61, 80, 45, 100]
analyze_scores(students_scores)
