# dynamodb-diff
DynamoDB-Diff is a tool to detect differences between two DynamoDB tables. It scans, sorts, and compares items to highlight discrepancies in key-value pairs. Perfect for debugging and maintaining database integrity.

## Features
- Compare two DynamoDB tables to find missing or differing items.
- Supports specifying a custom DynamoDB endpoint (e.g., for DynamoDB Local).
- Outputs the differences in a readable format.

## Development
### Prerequisites
- Python 3.8 or later
- `pipenv` for dependency management
- DynamoDB Local (optional, for local testing)

### Setup
```bash
pipenv install
pipenv shell
```

### Running Locally
To compare two tables using a specific DynamoDB endpoint (e.g., DynamoDB Local):
```bash
python src/main.py Table1Name Table2Name --endpoint_url http://localhost:8000
```

To compare tables using the default AWS DynamoDB endpoint:
```bash
python src/main.py Table1Name Table2Name
```

### Testing
Run the tests using `unittest`:
```bash
python -m unittest discover tests
```

## Build
To create a distributable package:
```bash
python setup.py sdist bdist_wheel
```

## Installation
To install the package locally:
```bash
pip install dist/dynamodb_diff-0.1.0.tar.gz
```

## Usage
After installing, use the `dynamodb-diff` command to compare tables:
```bash
dynamodb-diff Table1Name Table2Name
```

To use a specific DynamoDB endpoint:
```bash
dynamodb-diff Table1Name Table2Name --endpoint_url http://localhost:8000
```

## Examples
### Compare Tables with Default AWS Endpoint
```bash
dynamodb-diff ProductionTable1 ProductionTable2
```

### Compare Tables Using DynamoDB Local
```bash
dynamodb-diff TestTable1 TestTable2 --endpoint_url http://localhost:8000
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.
