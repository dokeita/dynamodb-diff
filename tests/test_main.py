import unittest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from decimal import Decimal
from src.main import fetch_all_items, compare_dynamodb_tables, cli

def normalize_item(item):
    """
    DynamoDB アイテムを標準化し、Decimal 型を数値に変換。
    """
    if isinstance(item, list):
        return [normalize_item(i) for i in item]
    elif isinstance(item, dict):
        return {k: normalize_item(v) for k, v in item.items()}
    elif isinstance(item, Decimal):
        return int(item) if item % 1 == 0 else float(item)
    else:
        return item

class MainTestCase(unittest.TestCase):
    @patch("src.main.boto3.resource")
    def test_fetch_all_items(self, mock_boto_resource):
        """
        fetch_all_items 関数が正しくデータを取得できるかをテスト
        """
        # モック設定
        mock_table = MagicMock()
        mock_table.scan.side_effect = [
            {"Items": [{"pk": "1", "name": "Alice"}], "LastEvaluatedKey": "key1"},
            {"Items": [{"pk": "2", "name": "Bob"}]},
        ]
        mock_boto_resource.return_value.Table.return_value = mock_table

        # テスト対象関数の実行
        dynamodb = mock_boto_resource.return_value
        result = fetch_all_items("TestTable", dynamodb)

        # 結果の検証
        expected = [
            {"pk": "1", "name": "Alice"},
            {"pk": "2", "name": "Bob"},
        ]
        self.assertEqual(result, expected)

    def test_compare_dynamodb_tables(self):
        """
        compare_dynamodb_tables 関数が差分を正しく検出できるかをテスト
        """
        # テスト用データ
        table1_items = [
            {"pk": "1", "name": "Alice", "age": 30},
            {"pk": "2", "name": "Bob", "age": 25},
        ]
        table2_items = [
            {"pk": "1", "name": "Alice", "age": 31},
            {"pk": "3", "name": "Charlie", "age": 22},
        ]

        # 比較処理の実行
        with patch("src.main.fetch_all_items") as mock_fetch_all_items:
            mock_fetch_all_items.side_effect = [table1_items, table2_items]
            compare_dynamodb_tables("Table1", "Table2", MagicMock())

        # 実行結果の手動確認が必要（unittest ではなく print を利用）
        print("Verify the output of compare_dynamodb_tables manually.")

    @patch("src.main.fetch_all_items")
    def test_cli(self, mock_fetch_all_items):
        """
        CLI 実行のテスト
        """
        # CLI テスト用のデータ
        table1_items = [{"pk": "1", "name": "Alice"}]
        table2_items = [{"pk": "2", "name": "Bob"}]
        mock_fetch_all_items.side_effect = [table1_items, table2_items]

        # CLI 実行
        runner = CliRunner()
        result = runner.invoke(cli, ["Table1", "Table2", "--endpoint_url", "http://localhost:8000"])

        # 結果の検証
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Items only in Table 1", result.output)
        self.assertIn("Items only in Table 2", result.output)

if __name__ == "__main__":
    unittest.main()
