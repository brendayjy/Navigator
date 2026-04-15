import datetime
import json
import re

class NavigatorTracker:
    def __init__(self, filename="navigator_data.json"):
        self.filename = filename
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.history = []
            
            
    def parse_plan_input(self, input_str):
        """解析简化输入，返回维度等级字典，未指定的维度默认为1"""
        MAX_LEVELS = {'T':10, 'O':8, 'L':10, 'F':4, 'M':19, 'Q':20, 'D':8}
        plan = {dim: 1 for dim in MAX_LEVELS}
        pattern = re.compile(r'([A-Z])(\d+)', re.IGNORECASE)
        for match in pattern.finditer(input_str.upper()):
            dim = match.group(1)
            level = int(match.group(2))
            if dim in MAX_LEVELS:
                if 1 <= level <= MAX_LEVELS[dim]:
                    plan[dim] = level
                else:
                    print(f"警告：{dim}{level} 超出范围（最大{MAX_LEVELS[dim]}），已忽略")
            else:
                print(f"警告：未知维度 {dim}，已忽略")
        return plan


    def record_session(self):
        print("--- 领航员行动：拿铁飞盘训练记录 ---")
        date = str(datetime.date.today())
        
        # 输入量化数据
        session_name = input("训练名称代码(例如MC1，字母代表名称 + 数字代表轮次):")
        description = input("训练内容描述: ")
        plan_input = input("今日训练等级 (例如 T3 O2，未写维度默认为1): ").strip()
        plan_levels = self.parse_plan_input(plan_input)
        integrity = float(input("动作完整度(1-5): "))
        linearity = float(input("直线返回评分 (1-5, 5为完美直线): "))
        arousal = float(input("兴奋度控制 (1-5, 5为极冷静): "))
        
        # 简单算法评估
        precision_factor = integrity * 10
        score = (precision_factor * linearity) / (6 - arousal)
        
        conclusion = self.analyze_progress(score)
        
        session = {
            "session_name": session_name,
            "description": description,
            "date": date,
            "plan_of_the_day":plan_input,
            "plan_levels": plan_levels,   # 存储计划等级字典
            "integrity": integrity,
            "linearity": linearity,
            "arousal": arousal,
            "score": round(score, 2),
            "conclusion": conclusion,

        }
        
        self.history.append(session)
        self.save_data()
        

    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=4, ensure_ascii=False)
        print("\n[系统记录已更新]")

    def analyze_progress(self, current_score):
        print(f"\n本日表现得分: {current_score}")
        if current_score > 80:
            conclusion = "表现优异！可以考虑进入下一难度等级或增加环境干扰。"
            print("结论：" + conclusion)
        elif current_score > 60:
            conclusion = "稳定进步中。维持当前强度。"
            print("结论：" + conclusion)
        else:
            conclusion = "系统过载。建议降低难度或退到更小、更安静的场地训练。"
            print("结论：" + conclusion)
        return conclusion


# 启动项目
if __name__ == "__main__":
    tracker = NavigatorTracker()
    tracker.record_session()