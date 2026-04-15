import json
import re

class NavigatorCompliance:
    def __init__(self):
        self.MAX_LEVELS = {
            'T': 10, 'O': 8, 'L': 10, 'F': 4,
            'M': 19, 'Q': 20, 'D': 8
        }
        self.HIGH_RISK = {'M', 'Q'}   # D 单独处理
        self.BASE_DIMS = {'T', 'L', 'O', 'F'}

    def input_baseline(self):
        baseline = {}
        print("\n请输入当前基准等级（最近一次成功通过的等级）：")
        for dim in self.MAX_LEVELS:
            while True:
                try:
                    val = int(input(f"  {dim} (1~{self.MAX_LEVELS[dim]}): "))
                    if 1 <= val <= self.MAX_LEVELS[dim]:
                        baseline[dim] = val
                        break
                    else:
                        print(f"  等级必须在 1~{self.MAX_LEVELS[dim]} 之间")
                except ValueError:
                    print("  请输入数字")
        return baseline

    def parse_plan_input(self, input_str, baseline):
        """解析简化输入，未指定的维度继承 baseline 的值"""
        plan = baseline.copy()   # 先复制 baseline
        pattern = re.compile(r'([A-Z])(\d+)', re.IGNORECASE)
        for match in pattern.finditer(input_str.upper()):
            dim = match.group(1)
            level = int(match.group(2))
            if dim in self.MAX_LEVELS:
                if 1 <= level <= self.MAX_LEVELS[dim]:
                    plan[dim] = level
                else:
                    print(f"警告：{dim}{level} 超出范围（最大{self.MAX_LEVELS[dim]}），已忽略")
            else:
                print(f"警告：未知维度 {dim}，已忽略")
        return plan

    def input_today_plan(self, baseline):
        print("\n请输入今日计划练习的维度及等级（例如：T3 O2，未写的维度保持原等级）：")
        while True:
            user_input = input("计划: ").strip().upper()
            if not user_input:
                print("输入不能为空，请重新输入")
                continue
            plan = self.parse_plan_input(user_input, baseline)
            # 显示完整计划让用户确认
            print("解析后的完整计划：")
            for dim in self.MAX_LEVELS:
                print(f"  {dim}: {plan[dim]}", end="  ")
            print()
            confirm = input("确认吗？(y/n): ").lower()
            if confirm == 'y':
                return plan

    def check_compliance(self, baseline, plan):
        violations = []
        warnings = []

        # 找出提升的维度（plan > baseline）
        upgraded = []
        for dim in self.MAX_LEVELS:
            diff = plan[dim] - baseline[dim]
            if diff > 0:
                upgraded.append((dim, diff))
            # 降低（diff < 0）允许，不记录为违规

        # 规则1：只能提升一个维度
        if len(upgraded) > 1:
            dims = ', '.join([d[0] for d in upgraded])
            violations.append(f"❌ 同时提升了 {len(upgraded)} 个维度 ({dims})。每次只能提升一个维度。")
        elif len(upgraded) == 1:
            dim, diff = upgraded[0]
            # 规则2：单级提升
            if diff > 1:
                violations.append(f"❌ {dim}: 尝试从 {baseline[dim]} 提升到 {plan[dim]}，单次只能提升1级。")
            
            # 规则3：D 维度的特殊回归
            if dim == 'D':
                if baseline['D'] == 1:
                    # 第一次提升 D：要求所有其他维度在 baseline 中已经是 1
                    other_dims = [d for d in self.MAX_LEVELS if d != 'D']
                    non_one = [d for d in other_dims if baseline[d] != 1]
                    if non_one:
                        violations.append(
                            f"❌ 第一次提升 D 时，所有其他维度必须已回归到 1。"
                            f"当前 baseline 中 {non_one} 不为 1。请先单独降低这些维度。"
                        )
                # 如果 baseline['D'] > 1，后续提升 D 无额外回归要求
            else:
                # 规则4：提升 M 或 Q 时，基础维度必须 ≤ 2
                if dim in self.HIGH_RISK:
                    unsafe = [d for d in self.BASE_DIMS if plan[d] > 2]
                    if unsafe:
                        violations.append(
                            f"❌ 提升了 {dim}，但基础维度 {unsafe} 未降至 1~2 级。"
                            f"（当前值 { {d: plan[d] for d in unsafe} }）"
                        )
        else:
            # 没有提升任何维度，只是巩固或降低
            pass

        # 额外提示：如果计划中主动降低了维度（不强制）
        regressed = [d for d in self.MAX_LEVELS if plan[d] < baseline[d]]
        if regressed and len(upgraded) == 0:
            warnings.append(f"💡 今日无提升，主动降低了 {regressed}，这是合理的回归练习。")

        return violations, warnings, [d[0] for d in upgraded]

    def run(self):
        print("=" * 60)
        print("   领航员行动：训练计划合规性检测器（单变量+螺旋回归）")
        print("=" * 60)

        baseline = self.input_baseline()
        plan = self.input_today_plan(baseline)

        violations, warnings, upgrades = self.check_compliance(baseline, plan)

        print("\n" + "-" * 60)
        if violations:
            print("❌ 计划不合规，请修正：")
            for v in violations:
                print(f"  {v}")
        else:
            print("✅ 计划合规！")
            if upgrades:
                print(f"  今日提升维度：{upgrades[0]} (单级进阶)")
                # 显示今天练习的所有维度（不同于 baseline 的部分）
                practiced = [d for d in self.MAX_LEVELS if plan[d] != baseline[d]]
                if practiced:
                    print(f"  今日练习的维度：{', '.join(practiced)}")
            else:
                print("  今日无维度提升，巩固或回归练习。")
        if warnings:
            print("\n📌 建议：")
            for w in warnings:
                print(f"  {w}")
        print("-" * 60)

if __name__ == "__main__":
    checker = NavigatorCompliance()
    checker.run()