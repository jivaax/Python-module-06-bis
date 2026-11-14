from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._data: list[str] = []
        self._processed_count = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._data:
            raise IndexError("No data available")
        rank = self._processed_count - len(self._data)
        value = self._data.pop(0)
        return (rank, value)


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            return all(isinstance(item, (int, float)) for item in data)
        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, list):
            values = [str(item) for item in data]
        else:
            values = [str(data)]
        self._data.extend(values)
        self._processed_count += len(values)


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return all(isinstance(item, str) for item in data)
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if isinstance(data, list):
            values = data.copy()
        else:
            values = [data]
        self._data.extend(values)
        self._processed_count += len(values)


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        def valid_log(item: Any) -> bool:
            return (
                isinstance(item, dict)
                and all(
                    isinstance(key, str) and isinstance(value, str)
                    for key, value in item.items()
                )
            )

        if isinstance(data, dict):
            return valid_log(data)
        if isinstance(data, list):
            return all(valid_log(item) for item in data)
        return False

    def ingest(
        self,
        data: dict[str, str] | list[dict[str, str]]
    ) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")

        logs = data if isinstance(data, list) else [data]
        values = []

        for log in logs:
            if "log_level" in log and "log_message" in log:
                value = f"{log['log_level']}: {log['log_message']}"
            else:
                value = str(log)
            values.append(value)

        self._data.extend(values)
        self._processed_count += len(values)


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===")

    numeric = NumericProcessor()
    print("\nTesting Numeric Processor...")
    print(f"Trying to validate input '42': {numeric.validate(42)}")
    print(
        "Trying to validate input 'Hello': "
        f"{numeric.validate('Hello')}"
    )
    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        numeric.ingest("foo")
    except ValueError as e:
        print(f"Got exception: {e}")

    numbers: list[int | float] = [1, 2, 3, 4, 5]
    print(f"Processing data: {numbers}")
    numeric.ingest(numbers)
    print("Extracting 3 values...")
    for _ in range(3):
        rank, value = numeric.output()
        print(f"Numeric value {rank}: {value}")

    text = TextProcessor()
    print("\nTesting Text Processor...")
    print(f"Trying to validate input '42': {text.validate(42)}")
    words = ["Hello", "Nexus", "World"]
    print(f"Processing data: {words}")
    text.ingest(words)
    print("Extracting 1 value...")
    rank, value = text.output()
    print(f"Text value {rank}: {value}")

    logs = LogProcessor()
    print("\nTesting Log Processor...")
    print(f"Trying to validate input 'Hello': {logs.validate('Hello')}")
    log_data = [
        {
            "log_level": "NOTICE",
            "log_message": "Connection to server"
        },
        {
            "log_level": "ERROR",
            "log_message": "Unauthorized access!!"
        }
    ]
    print(f"Processing data: {log_data}")
    logs.ingest(log_data)
    print("Extracting 2 values...")
    for _ in range(2):
        rank, value = logs.output()
        print(f"Log entry {rank}: {value}")
