
from typing import Any, Protocol

from data_processor import (
    DataProcessor,
    NumericProcessor,
    TextProcessor,
    LogProcessor
)


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class CSVExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        values = [value for _, value in data]
        escaped = [
            '"' + value.replace('"', '""') + '"'
            if any(char in value for char in [",", '"', "\n", "\r"])
            else value
            for value in values
        ]
        print("CSV Output:")
        print(",".join(escaped))


class JSONExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        def escape_json(value: str) -> str:
            result = ""
            for char in value:
                if char == '"':
                    result += '\\"'
                elif char == "\\":
                    result += "\\\\"
                elif char == "\n":
                    result += "\\n"
                elif char == "\r":
                    result += "\\r"
                elif char == "\t":
                    result += "\\t"
                elif ord(char) < 32:
                    result += f"\\u{ord(char):04x}"
                else:
                    result += char
            return result

        entries = [
            f'"item_{rank}": "{escape_json(value)}"'
            for rank, value in data
        ]
        print("JSON Output:")
        print("{" + ", ".join(entries) + "}")


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            processed = False

            for processor in self._processors:
                if processor.validate(element):
                    processor.ingest(element)
                    processed = True
                    break

            if not processed:
                print(
                    "DataStream error - Can't process element in stream: "
                    f"{element}"
                )

    def print_processors_stats(self) -> None:
        print("\n== DataStream statistics ==")

        if not self._processors:
            print("No processor found, no data")
            return

        for processor in self._processors:
            name = type(processor).__name__.replace(
                "Processor", " Processor"
            )
            total = processor._processed_count
            remaining = len(processor._data)

            print(
                f"{name}: total {total} items processed, "
                f"remaining {remaining} on processor"
            )

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        if nb < 0:
            raise ValueError("Number of items cannot be negative")

        if nb == 0:
            return

        for processor in self._processors:
            output_data: list[tuple[int, str]] = []

            for _ in range(min(nb, len(processor._data))):
                output_data.append(processor.output())

            if output_data:
                plugin.process_output(output_data)


if __name__ == "__main__":
    print("=== Code Nexus - Data Pipeline ===")

    stream = DataStream()

    print("\nInitialize Data Stream...")
    stream.print_processors_stats()

    numeric = NumericProcessor()
    text = TextProcessor()
    logs = LogProcessor()

    print("\nRegistering Processors")
    stream.register_processor(numeric)
    stream.register_processor(text)
    stream.register_processor(logs)

    batch1: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead"
            },
            {
                "log_level": "INFO",
                "log_message": "User wil is connected"
            }
        ],
        42,
        ["Hi", "five"]
    ]

    print(f"\nSend first batch of data on stream: {batch1}")
    stream.process_stream(batch1)
    stream.print_processors_stats()

    print("\nSend 3 processed data from each processor to a CSV plugin:")
    stream.output_pipeline(3, CSVExportPlugin())
    stream.print_processors_stats()

    batch2: list[Any] = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {
                "log_level": "ERROR",
                "log_message": "500 server crash"
            },
            {
                "log_level": "NOTICE",
                "log_message": "Certificate expires in 10 days"
            }
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello"
    ]

    print(f"\nSend another batch of data: {batch2}")
    stream.process_stream(batch2)
    stream.print_processors_stats()

    print("\nSend 5 processed data from each processor to a JSON plugin:")
    stream.output_pipeline(5, JSONExportPlugin())
    stream.print_processors_stats()
