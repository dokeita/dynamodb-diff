from io import StringIO
import unittest
from unittest.mock import patch
import boto3
from decimal import Decimal
from src.main import fetch_all_items, compare_dynamodb_tables

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

class IntegrationTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        DynamoDB Local の設定
        """
        cls.endpoint_url = "http://localhost:8000"
        cls.dynamodb = boto3.resource(
            "dynamodb",
            endpoint_url=cls.endpoint_url,
        )

    def setUp(self):
        """
        各テストの前にテーブルを作成し、データを登録する
        """
        # テーブル 1 の作成
        self.table1 = self.dynamodb.create_table(
            TableName="TestTable1",
            KeySchema=[{"AttributeName": "pk", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "pk", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        self.table1.wait_until_exists()

        # テーブル 2 の作成
        self.table2 = self.dynamodb.create_table(
            TableName="TestTable2",
            KeySchema=[{"AttributeName": "pk", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "pk", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        self.table2.wait_until_exists()

        # テーブル 1 にデータを登録
        self.table1.put_item(Item={"pk": "1", "name": "Alice", "age": Decimal(30)})
        self.table1.put_item(Item={"pk": "2", "name": "Bob", "age": Decimal(25)})

        # テーブル 2 にデータを登録
        self.table2.put_item(Item={"pk": "1", "name": "Alice", "age": Decimal(31)})
        self.table2.put_item(Item={"pk": "3", "name": "Charlie", "age": Decimal(22)})

    def tearDown(self):
        """
        各テストの後にテーブルを削除する
        """
        self.table1.delete()
        self.table2.delete()
        self.table1.wait_until_not_exists()
        self.table2.wait_until_not_exists()

    def test_fetch_all_items(self):
        """
        fetch_all_items 関数が正しくデータを取得できるかをテスト
        """
        result = normalize_item(fetch_all_items("TestTable1", self.dynamodb))
        expected = [
            {"pk": "1", "name": "Alice", "age": 30},
            {"pk": "2", "name": "Bob", "age": 25},
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
