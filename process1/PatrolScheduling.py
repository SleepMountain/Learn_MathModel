import random


#小区1老保安和新保安列表
old_security = ["凌*涌", "许*龙", "茹*勇", "覃*才", "朱*杰", "阮*飞", "黄*均", "佘*红"]
new_security = ["肖*同", "张*贵", "马*鑫", "金*", "何*", "罗*新", "徐*相", "尉*", "陈*杰"]
# 队长列表
captains = ["许*龙", "朱*杰", "罗*新"]
#小区2老保安和新保安列表
"""
old_security = ["詹*江", "李*国", "赵*贵", "翟*发", "诸*敏", "周*永", "原*林", "沈*新"]
new_security = ["傅*平", "王*华", "庞*华", "程*林", "龚*华", "黄*熊", "吴*连", "陈*华", "刘*英"]
# 队长列表
captains = ["原*林", "吴*连", "刘*英"]
"""
#小区3老保安和新保安列表
"""
old_security = ["马*勤", "徐*炜", "李*兵", "周*通", "伍*云", "管*任", "李*斌", "俞*贤", "陈*友"]
new_security = ["高*锋", "吴*飞", "杨*东", "戚*红", "张*凤", "陈*民", "蒋*锋", "周*华"]
# 队长列表
captains = ["管*任", "张*凤", "周*华"]
"""
#小区4老保安和新保安列表
"""
old_security = ["程*庆", "曹*军", "韦*兵", "郑*强", "顾*聪", "韦*", "孙*生", "徐*锋", "张*领"]
new_security = ["贾*荣", "裘*明", "文*方", "孙*", "孔*明", "胡*林", "邱*军", "赵*生"]
# 队长列表
captains = ["顾*聪", "徐*锋", "赵*生"]
"""
#小区5老保安和新保安列表
"""
old_security = ["祝*良", "张*明", "冉*", "周*林", "孙*兴", "齐*", "许*明", "李*峰", "李*伟"]
new_security = ["谢*偶", "朱*创", "蒋*勇", "刘*红", "王*龙", "韩*", "张*龙", "党*新"]
# 队长列表
captains = ["许*明", "张*龙","许*明."]
"""
#小区6老保安和新保安列表
"""
old_security = ["高*杰", "包*花", "邱*良", "周*军", "高*先", "徐*文", "邓*彬", "宋*东"]
new_security = ["李*天", "程*喜", "孔*林", "郑*天", "李*芳", "吴*华", "汤*凤", "翟*宝", "王*喜"]
# 队长列表
captains = ["包*花", "邓*彬", "王*喜"]
"""
#小区7老保安和新保安列表
"""
old_security = ["陈*明", "欧*文珍", "李*收", "袁*杰", "金*林", "覃*燕", "郝*松", "郭*焕", "许*华"]
new_security = ["张*坤", "李*春", "瞿*庆", "徐*武", "李*富", "盛*明", "侯*敏", "林*辉"]
# 队长列表
captains = ["金*林", "侯*敏", "金*林."]
"""
#小区8老保安和新保安列表
"""
old_security = ["解*洋", "陈*山", "明*英", "叶*元", "李*影", "周*", "谢*丹", "王*响", "汪*栋"]
new_security = ["章*", "王*福", "杜*富", "张*芬", "郝*子", "解*坡", "孟*雷", "邱*贵"]
# 队长列表
captains = ["周*", "孟*雷", "周*."]
"""

# 班次列表
shifts = ["0-8", "8-16", "16-24"]

# 初始化巡逻安排
patrol_schedule = []

# 初始化保安的巡逻情况记录，如连续巡逻天数和巡逻班次安排
security_records = {}

# 按照入职年限对老保安和新保安进行排序
old_security.sort()
new_security.sort()

# 随机打乱老保安和新保安的顺序
random.shuffle(old_security)
random.shuffle(new_security)


def select_security(s_type):
    """
    选择一个保安（老保安或新保安）
    """
    if s_type == "old":
        return old_security.pop(0)
    else:
        return new_security.pop(0)


def is_valid(security, shift):
    """
    判断保安在某一班次是否合法（满足排他性和公平性要求）
    """
    # 判断队长是否在同一班次
    if security in captains and any(schedule["队长"] == security for schedule in patrol_schedule):
        return False

    # 判断保安是否连续巡逻超过3天
    if security_records.get(security, 0) >= 3:
        return False

    # 判断保安是否总是在同一班次巡逻
    if any(schedule["保安"] == security for schedule in patrol_schedule[-2:]):
        return False

    return True


# 按照班次顺序进行巡逻安排
for shift in shifts:
    # 初始化当前班次的巡逻安排
    current_schedule = {"班次": shift, "保安": [], "队长": ""}

    # 选择老保安和新保安，需老保安搭配新保安
    old_security_personnel = select_security("old")
    new_security_personnel = select_security("new")

    # 随机选择队长
    captain = random.choice(captains)

    # 判断保安和队长的合法性，直到找到合适的保安和队长
    while not is_valid(old_security_personnel, shift) or not is_valid(new_security_personnel, shift) or captain in [
        schedule["队长"] for schedule in patrol_schedule]:
        old_security.append(old_security_personnel)
        new_security.append(new_security_personnel)
        random.shuffle(old_security)
        random.shuffle(new_security)
        old_security_personnel = select_security("old")
        new_security_personnel = select_security("new")
        captain = random.choice(captains)

    # 添加保安和队长到巡逻安排中
    current_schedule["保安"].extend([old_security_personnel, new_security_personnel])
    current_schedule["队长"] = captain

    # 更新保安的巡逻情况记录
    security_records[old_security_personnel] = security_records.get(old_security_personnel, 0) + 1
    security_records[new_security_personnel] = security_records.get(new_security_personnel, 0) + 1

    # 添加当前班次的巡逻安排到总的巡逻安排列表中
    patrol_schedule.append(current_schedule)

# 打印巡逻安排结果
for schedule in patrol_schedule:
    print(f"班次: {schedule['班次']}, 保安: {', '.join(schedule['保安'])}, 队长: {schedule['队长']}")
