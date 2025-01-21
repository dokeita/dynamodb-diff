import click
import boto3
from botocore.exceptions import ClientError

def fetch_all_items(table_name, dynamodb):
    """
    DynamoDB テーブルからすべてのアイテムを取得し、各アイテムをキー順にソート。
    """
    table = dynamodb.Table(table_name)
    try:
        response = table.scan()
        items = []

        # 現在のページのアイテムをソートして追加
        sorted_items = [sort_dict_by_keys(item) for item in response.get('Items', [])]
        items.extend(sorted_items)

        # ページング処理
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            sorted_items = [sort_dict_by_keys(item) for item in response.get('Items', [])]
            items.extend(sorted_items)

        return items
    except ClientError as e:
        print(f"Error fetching items from {table_name}: {e}")
        return []

def sort_dict_by_keys(item):
    """
    辞書をキーのアルファベット順でソートしてタプル化。
    """
    return dict(sorted(item.items()))

def compare_dynamodb_tables(table1_name, table2_name, dynamodb):
    """
    2つの DynamoDB テーブルを比較し、差分を出力。
    """
    table1_items = fetch_all_items(table1_name, dynamodb)
    table2_items = fetch_all_items(table2_name, dynamodb)

    # ソート後のアイテムをタプル化して比較
    table1_set = {tuple(sorted(item.items())) for item in table1_items}
    table2_set = {tuple(sorted(item.items())) for item in table2_items}

    only_in_table1 = table1_set - table2_set
    only_in_table2 = table2_set - table1_set

    # 結果出力
    print("Items only in Table 1:")
    for item in only_in_table1:
        print(dict(item))

    print("\nItems only in Table 2:")
    for item in only_in_table2:
        print(dict(item))

@click.command()
@click.argument("table1_name")
@click.argument("table2_name")
@click.option(
    "--endpoint_url", "-e", 
    default=None, 
    help="Specify the DynamoDB endpoint URL (e.g., http://localhost:8000)."
)
def cli(table1_name, table2_name, endpoint_url):
    """
    CLI エントリポイント: DynamoDB テーブルを比較する
    """
    # DynamoDB リソースを設定
    dynamodb_args = {
        # "region_name": "us-west-2",
        # "aws_access_key_id": "dummy",
        # "aws_secret_access_key": "dummy",
    }
    if endpoint_url:
        dynamodb_args["endpoint_url"] = endpoint_url

    dynamodb = boto3.resource("dynamodb", **dynamodb_args)

    # テーブル比較の実行
    compare_dynamodb_tables(table1_name, table2_name, dynamodb)

if __name__ == "__main__":
    cli()
