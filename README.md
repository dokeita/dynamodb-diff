# dynamodb-diff
DynamoDB-Diff is a tool to detect differences between two DynamoDB tables. It scans, sorts, and compares items to highlight discrepancies in key-value pairs. Perfect for debugging and maintaining database integrity.

## Development
```bash
pipenv install
pipenv shell
python src/main.py Table1Name Table2Name
```

### Build
```bash
python setup.py sdist bdist_wheel
```

## Installation
```bash
pip install dist/dynamodb_diff-0.1.0.tar.gz
```
## Usage
```bash
dynamodb-diff Table1Name Table2Name
```
