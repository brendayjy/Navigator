import datetime
import json

class NavigatorTracker:
    def __init__(self, filename="navigator_data.json"):
        self.filename = filename
        try:
            with open(self.filename, 'r') as f:
                self.history = json.load(f)
        except FileNotFoundError:
            self.history = []

    def record_session(self):
        print("--- 领航员行动：每日训练记录 ---")
        date = str(datetime.date.today())
        
        # 输入量化数据
        stay_time = int(input("最高等待时长 (秒): "))
        distance = int(input("最大脱敏距离 (米): "))
        linearity = int(input("直线返回评分 (1-5, 5为完美直线): "))
        arousal = int(input("兴奋度控制 (1-5, 5为极冷静): "))
        
        # 简单算法评估
        score = (stay_time * distance * linearity) / (6 - arousal)
        
        session = {
            "date": date,
            "stay_time": stay_time,
            "distance": distance,
            "linearity": linearity,
            "arousal": arousal,
            "score": round(score, 2)
        }
        
        self.history.append(session)
        self.save_data()
        self.analyze_progress(score)

    def save_data(self):
        with open(self.filename, 'w') as f:
            json.dump(self.history, f, indent=4)
        print("\n[系统记录已更新]")

    def analyze_progress(self, current_score):
        print(f"\n本日表现得分: {current_score}")
        if current_score > 100:
            print("结论：表现优异！可以考虑增加环境干扰。")
        elif current_score > 50:
            print("结论：稳定进步中。维持当前强度。")
        else:
            print("结论：系统过载。建议回退到更小、更安静的场地训练。")

# 启动项目
if __name__ == "__main__":
    tracker = NavigatorTracker()
    tracker.record_session()