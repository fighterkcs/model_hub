import re
from tool import CalculatorTool, WeatherTool

class CalculatorAgent:
    def __init__(self):
        self.tool = CalculatorTool()

    def perform_task(self, prompt):
        nums = list(map(int, re.findall(r"\d+", prompt)))
        if len(nums) < 2:
            return None

        text = prompt.lower()

        if "add" in text or "plus" in text:
            return self.tool.add(nums[0], nums[1])
        if "subtract" in text or "minus" in text:
            return self.tool.subtract(nums[0], nums[1])
        if "multiply" in text or "times" in text:
            return self.tool.multiply(nums[0], nums[1])
        if "divide" in text:
            return self.tool.divide(nums[0], nums[1])

        return None


class WeatherAgent:
    def __init__(self, api_key):
        self.tool = WeatherTool(api_key)

    def perform_task(self, prompt):
        match = re.search(r"weather in ([\w\s]+)", prompt, re.IGNORECASE)
        if match:
            return self.tool.perform_task(match.group(1).strip())
        return None


class Agent:
    def __init__(self, api_key):
        self.agents = [
            CalculatorAgent(),
            WeatherAgent(api_key)
        ]

    def perform_task(self, prompt):
        for agent in self.agents:
            result = agent.perform_task(prompt)
            if result is not None:
                return result
        return None
