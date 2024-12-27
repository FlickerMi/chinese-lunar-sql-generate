from datetime import datetime, timedelta
import zhdate
import ephem
from typing import List, Tuple

class CalendarHelper:
    def __init__(self):
        # 定义节气
        self.solar_terms = [
            "小寒", "大寒", "立春", "雨水", "惊蛰", "春分",
            "清明", "谷雨", "立夏", "小满", "芒种", "夏至",
            "小暑", "大暑", "立秋", "处暑", "白露", "秋分",
            "寒露", "霜降", "立冬", "小雪", "大雪", "冬至"
        ]
        
        # 定义公历节日
        self.solar_festivals = {
            "0101": "元旦",
            "0214": "情人节",
            "0308": "妇女节",
            "0312": "植树节",
            "0401": "愚人节",
            "0501": "劳动节",
            "0504": "青年节",
            "0601": "儿童节",
            "0701": "建党节",
            "0801": "建军节",
            "0910": "教师节",
            "1001": "国庆节",
            "1024": "联合国日",
            "1225": "圣诞节"
        }
        
        # 定义农历节日
        self.lunar_festivals = {
            "0101": "春节",
            "0115": "元宵节",
            "0505": "端午节",
            "0707": "七夕节",
            "0715": "中元节",
            "0815": "中秋节",
            "0909": "重阳节",
            "1208": "腊八节",
            "1223": "小年",
            "1230": "除夕"  # 农历最后一天
        }
        
        # 定义纪念日
        self.memorial_days = {
            "0127": "国际大屠杀纪念日",
            "0413": "清明节 黄帝故里拜祖大典",
            "0504": "中国青年节 五四运动纪念日",
            "0512": "全国防灾减灾日 汶川地震纪念日",
            "0701": "香港回归纪念日",
            "0707": "抗日战争纪念日",
            "0918": "九一八事变纪念日",
            "1213": "南京大屠杀死难者国家公祭日"
        }

    def get_solar_term(self, date: datetime) -> str:
        """获取节气"""
        year = date.year
        solar_terms_dates = []

        # 计算指定年份的节气日期
        j = 0
        for i in range(24):
            # 按照节气推算公式计算
            jd = ephem.next_solstice(str(year)) if i > 11 else ephem.next_equinox(str(year))
            jd = ephem.Date(jd + i * 15.2 / 360)
            date_str = ephem.Date(jd).datetime().strftime('%Y-%m-%d')
            solar_terms_dates.append((date_str, self.solar_terms[i]))

        # 检查当前日期是否为节气
        current_date_str = date.strftime('%Y-%m-%d')
        for term_date, term_name in solar_terms_dates:
            if term_date == current_date_str:
                return term_name
        return None

    def get_lunar_month_days(self, lunar_year: int, lunar_month: int, is_leap: bool = False) -> int:
        """获取农历月份的天数"""
        try:
            # 获取当月第一天
            current_month = zhdate.ZhDate(lunar_year, lunar_month, 1)
            
            if lunar_month == 12:
                # 处理腊月
                next_year = zhdate.ZhDate(lunar_year + 1, 1, 1)
                days = (next_year.to_datetime() - current_month.to_datetime()).days
            else:
                # 获取下个月第一天
                next_month = zhdate.ZhDate(lunar_year, lunar_month + 1, 1)
                days = (next_month.to_datetime() - current_month.to_datetime()).days
            
            return days
        except:
            # 默认返回30天
            return 30

    def get_festivals(self, date: datetime, lunar_date: zhdate.ZhDate) -> Tuple[str, str]:
        """获取节日和纪念日"""
        solar_date_str = date.strftime('%m%d')
        # 修改获取农历日期字符串的方式
        lunar_date_str = f"{lunar_date.lunar_month:02d}{lunar_date.lunar_day:02d}"

        festivals = []
        memorial_days = []

        # 获取公历节日
        if solar_date_str in self.solar_festivals:
            festivals.append(self.solar_festivals[solar_date_str])

        # 获取农历节日
        if lunar_date_str in self.lunar_festivals:
            # 对于除夕特殊处理
            if lunar_date_str == "1230":
                # 检查是否为当月最后一天
                days_in_month = self.get_lunar_month_days(lunar_date.lunar_year, lunar_date.lunar_month)
                if lunar_date.lunar_day != days_in_month:
                    # 如果不是月末，则不是除夕
                    festivals.append(self.lunar_festivals[lunar_date_str])
            else:
                festivals.append(self.lunar_festivals[lunar_date_str])
        else:
            # 检查是否为除夕（月末）
            if lunar_date.lunar_month == 12:  # 如果是腊月
                days_in_month = self.get_lunar_month_days(lunar_date.lunar_year, lunar_date.lunar_month)
                if lunar_date.lunar_day == days_in_month:  # 如果是月末
                    festivals.append("除夕")

        # 获取节气
        term = self.get_solar_term(date)
        if term:
            festivals.append(term)

        # 获取纪念日
        if solar_date_str in self.memorial_days:
            memorial_days.append(self.memorial_days[solar_date_str])

        return (
            ' '.join(festivals) if festivals else None,
            ' '.join(memorial_days) if memorial_days else None
        )

def get_zodiac_animal(lunar_year: int) -> str:
    """
    根据农历年份获取生肖
    参数：
        lunar_year: 农历年份
    返回：
        对应的生肖
    """
    animals = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']
    return animals[(lunar_year - 4) % 12]

def get_cn_day(weekday: int) -> str:
    """
    获取星期的中文表示
    参数：
        weekday: 0-6 代表周一到周日
    返回：
        中文星期表示
    """
    days = ['一', '二', '三', '四', '五', '六', '日']
    return days[weekday]

def get_gz_year(lunar_year: int) -> str:
    """
    获取年份的干支纪年
    参数：
        lunar_year: 农历年份
    返回：
        干支纪年字符串
    """
    heavenly_stems = "甲乙丙丁戊己庚辛壬癸"
    earthly_branches = "子丑寅卯辰巳午未申酉戌亥"
    
    # 农历年份减3 （说明：补减1）
    year = lunar_year - 3 - 1
    G = year % 10  # 模10，得到天干数
    Z = year % 12  # 模12，得到地支数
    return heavenly_stems[G] + earthly_branches[Z]

def get_gz_month(lunar_month: int, lunar_year: int) -> str:
    """
    获取月份的干支纪月
    参数：
        lunar_month: 农历月份
        lunar_year: 农历年份
    返回：
        干支纪月字符串
    """
    heavenly_stems = "甲乙丙丁戊己庚辛壬癸"
    earthly_branches = "子丑寅卯辰巳午未申酉戌亥"
    
    # 确定年干支
    year_stem_index = (lunar_year - 4) % 10  # 1984年为甲子年
    
    # 确定正月（寅月）的天干
    # 甲己年起丙寅，乙庚年起戊寅，丙辛年起庚寅，丁壬年起壬寅，戊癸年起甲寅
    first_month_stem_map = {
        0: 2,  # 甲年起丙
        5: 2,  # 己年起丙
        1: 4,  # 乙年起戊
        6: 4,  # 庚年起戊
        2: 6,  # 丙年起庚
        7: 6,  # 辛年起庚
        3: 8,  # 丁年起壬
        8: 8,  # 壬年起壬
        4: 0,  # 戊年起甲
        9: 0   # 癸年起甲
    }
    
    # 确定正月的天干
    first_month_stem = first_month_stem_map[year_stem_index]
    
    # 计算当前月份的天干
    # 从正月（寅月）开始，每个月天干依次推进
    stem_index = (first_month_stem + ((lunar_month - 1) % 12)) % 10
    
    # 计算当前月份的地支
    # 正月对应寅，依次类推
    branch_index = ((lunar_month + 1) % 12)  # +1是因为正月对应寅（寅是地支的第三位）
    
    return heavenly_stems[stem_index] + earthly_branches[branch_index]

def get_gz_day(date: datetime) -> str:
    """
    获取日期的干支纪日
    参数：
        date: datetime对象
    返回：
        干支纪日字符串
    """
    heavenly_stems = "甲乙丙丁戊己庚辛壬癸"
    earthly_branches = "子丑寅卯辰巳午未申酉戌亥"
    
    # 取世纪数
    C = date.year // 100
    # 取年份后两位（若为1月、2月则当前年份减一）
    y = date.year % 100
    y = y - 1 if date.month == 1 or date.month == 2 else y
    # 取月份（若为1月、2月则分别按13、14来计算）
    M = date.month
    M = M + 12 if date.month == 1 or date.month == 2 else M
    # 取日数
    d = date.day
    # 取i （奇数月i=0，偶数月i=6）
    i = 0 if date.month % 2 == 1 else 6
    
    # 计算干（说明：补减1）
    G = 4 * C + C // 4 + 5 * y + y // 4 + 3 * (M + 1) // 5 + d - 3 - 1
    G = G % 10
    # 计算支（说明：补减1）
    Z = 8 * C + C // 4 + 5 * y + y // 4 + 3 * (M + 1) // 5 + d + 7 + i - 1
    Z = Z % 12
    
    return heavenly_stems[G] + earthly_branches[Z]

def get_lunar_day(day: int) -> str:
    """
    获取农历日期的中文表示
    参数：
        day: 农历日期数字
    返回：
        农历日期的中文表示
    """
    if day == 30:
        return "三十"

    tens = ['初', '十', '廿']
    ones = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']

    if day == 20:
        return "二十"
    elif day == 10:
        return "初十"

    tens_digit = (day - 1) // 10
    ones_digit = (day - 1) % 10

    result = tens[tens_digit]
    if ones_digit != 9:  # 非'十'的情况
        result += ones[ones_digit]

    return result


def generate_calendar_data(start_date_str: str, end_date_str: str) -> str:
    """生成指定时间段的万年历数据"""
    calendar_helper = CalendarHelper()
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    current_date = start_date

    insert_statements = []
    insert_template = """INSERT INTO `olm`.`olm_days` 
(`id`, `animal`, `cnDay`, `day`, `gzDate`, `gzMonth`, `gzYear`, `isBigMonth`, `lDate`, `lMonth`, `lunarDate`, `lunarMonth`, `lunarYear`, `month`, `oDate`, `status`, `suit`, `avoid`, `term`, `bvalue`, `year`, `stype`, `desc`) VALUES 
"""

    while current_date <= end_date:
        # 获取农历日期
        lunar_date = zhdate.ZhDate.from_datetime(current_date)
        
        # 获取节日和纪念日
        term, bvalue = calendar_helper.get_festivals(current_date, lunar_date)

        # 判断是否为大月
        is_big_month = calendar_helper.get_lunar_month_days(lunar_date.lunar_year, lunar_date.lunar_month) == 30

        # 处理闰月的显示
        lunar_month_display = str(lunar_date.lunar_month)
        if lunar_date.lunar_month > 12:  # 闰月的情况
            actual_month = lunar_date.lunar_month - 12
            lunar_month_display = f"闰{actual_month}"
            
        # 生成数据行
        row_data = {
            'id': current_date.strftime("%Y%m%d"),
            'animal': get_zodiac_animal(lunar_date.lunar_year),
            'cnDay': get_cn_day(current_date.weekday()),
            'day': current_date.day,
            'gzDate': get_gz_day(current_date),
            'gzMonth': get_gz_month(lunar_date.lunar_month if lunar_date.lunar_month <= 12 
                                  else lunar_date.lunar_month - 12, lunar_date.lunar_year),
            'gzYear': get_gz_year(lunar_date.lunar_year),
            'isBigMonth': '1' if is_big_month else '0',
            'lDate': get_lunar_day(lunar_date.lunar_day),
            'lMonth': lunar_month_display,
            'lunarDate': lunar_date.lunar_day,
            'lunarMonth': lunar_date.lunar_month if lunar_date.lunar_month <= 12 
                         else lunar_date.lunar_month - 12,
            'lunarYear': lunar_date.lunar_year,
            'month': current_date.month,
            'oDate': (current_date - timedelta(hours=8)).strftime("%Y-%m-%dT%H:00:00.000Z"),
            'status': '0',
            'suit': '', # TODO 宜忌信息需要另外添加
            'avoid': '', # TODO 宜忌信息需要另外添加
            'term': f"'{term}'" if term else 'NULL',
            'bvalue': f"'{bvalue}'" if bvalue else 'NULL',
            'year': current_date.year,
            'stype': 'NULL',
            'desc': 'NULL'
        }

        # 生成INSERT语句
        values = f"""({row_data['id']}, '{row_data['animal']}', '{row_data['cnDay']}', {row_data['day']}, '{row_data['gzDate']}', '{row_data['gzMonth']}', '{row_data['gzYear']}', '{row_data['isBigMonth']}', '{row_data['lDate']}', '{row_data['lMonth']}', {row_data['lunarDate']}, {row_data['lunarMonth']}, {row_data['lunarYear']}, {row_data['month']}, '{row_data['oDate']}', {row_data['status']}, '{row_data['suit']}', '{row_data['avoid']}', {row_data['term']}, {row_data['bvalue']}, {row_data['year']}, {row_data['stype']}, {row_data['desc']})"""

        insert_statements.append(values)
        current_date += timedelta(days=1)

    return insert_template + ',\n'.join(insert_statements) + ';'

# 使用示例
if __name__ == "__main__":
    
    # 生成2025年1月的数据
    sql = generate_calendar_data('2025-01-01', '2025-12-31')
    
    # 将生成的SQL语句保存到文件
    with open('calendar_data.sql', 'w', encoding='utf-8') as f:
        f.write(sql)