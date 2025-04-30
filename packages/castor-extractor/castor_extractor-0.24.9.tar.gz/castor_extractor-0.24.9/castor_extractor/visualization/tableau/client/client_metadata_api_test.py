from .client_metadata_api import _deduplicate


def test__deduplicate():
    result_pages = iter(
        [
            [
                {"id": 1, "name": "workbook_1"},
                {"id": 2, "name": "workbook_2"},
            ],
            [
                {"id": 1, "name": "workbook_1"},
                {"id": 3, "name": "workbook_3"},
                {"id": 4, "name": "workbook_4"},
            ],
            [
                {"id": 4, "name": "workbook_4"},
                {"id": 5, "name": "workbook_5"},
                {"id": 5, "name": "workbook_5"},
                {"id": 5, "name": "workbook_5"},
            ],
            [
                {"id": 1, "name": "workbook_1"},
                {"id": 3, "name": "workbook_3"},
            ],
        ]
    )
    deduplicated = _deduplicate(result_pages)
    assert len(deduplicated) == 5
    deduplicated_keys = {item["id"] for item in deduplicated}
    assert deduplicated_keys == {1, 2, 3, 4, 5}
