import json
from enum import Enum
from datetime import datetime
from dataclasses import dataclass

from datasets import load_dataset


@dataclass
class Test:
    input: str
    output: str
    testtype: str


@dataclass
class TestOutputPredictionProblem:
    question_title: str
    question_content: str
    question_id: str
    contest_id: str
    contest_date: datetime
    difficulty: str
    test: list[Test]
    starter_code: str
    function_name: str
    test_id: int

    def __post_init__(self):
        self.test = [Test(**t) for t in json.loads(self.test)]

    def insert_output(self, output_list: list[str], pred_list: list[str]) -> dict:
        return {
            "question_title": self.question_title,
            "question_content": self.question_content,
            "question_id": self.question_id,
            "contest_id": self.contest_id,
            "contest_date": self.contest_date.isoformat(),
            "difficulty": self.difficulty,
            "output_list": output_list,
            "pred_list": pred_list,
            "test_id": self.test_id,
            "function_name": self.function_name,
            "starter_code": self.starter_code,
        }

    def get_evaluation_sample(self) -> dict:
        return {
            "input": self.question_content,
            "output": self.test[0].output,
        }


def load_test_prediction_dataset() -> list[TestOutputPredictionProblem]:
    dataset = load_dataset("livecodebench/test_generation", split="test")
    print(dataset[0].keys())
    dataset = [TestOutputPredictionProblem(**d) for d in dataset]
    print(f"Loaded {len(dataset)} prediction problems")
    return dataset


if __name__ == "__main__":
    dataset = load_test_prediction_dataset()
