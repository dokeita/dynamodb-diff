import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')


def fetch_all_items(table_name):
    """
    DynamoDB テーブルからすべてのアイテムを取得し、各アイテムをキー順にソート。
    """
    table = dynamodb.Table(table_name)
    try:
        response = table.scan()
        items = []

        # 現在のページのアイテムをソートして追加
        sorted_items = [
            sort_dict_by_keys(item) for item in response.get('Items', [])
        ]
        items.extend(sorted_items)

        while 'LastEvaluatedKey' in response:
            response = table.scan(
                ExclusiveStartKey=response['LastEvaluatedKey'])
            sorted_items = [
                sort_dict_by_keys(item) for item in response.get('Items', [])
            ]
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


def compare_dynamodb_tables(table1_name, table2_name):
    """
    2つの DynamoDB テーブルのアイテムを比較して結果を出力。
    """
    table1_items = fetch_all_items(table1_name)
    table2_items = fetch_all_items(table2_name)

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


# # 実行例
# compare_dynamodb_tables("table1_name", "table2_name")
