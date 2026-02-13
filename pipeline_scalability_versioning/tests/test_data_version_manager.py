from src.data_version_manager import DataVersionManager


def test_validate_v1_ok():
    vm = DataVersionManager()
    data = {"schema_version": 1, "id": "1", "name": "A", "created_at": "2024-01-01T00:00:00"}
    result = vm.validate_schema(data)
    assert result["valid"] is True


def test_upgrade_v1_to_v3_and_validate_ok():
    vm = DataVersionManager()
    legacy = {"schema_version": 1, "id": "1", "name": "A", "created_at": "2024-01-01T00:00:00"}
    upgraded = vm.upgrade_data(legacy, 3)

    assert upgraded["schema_version"] == 3
    assert "email" in upgraded and upgraded["email"] is None
    assert "phone" in upgraded and upgraded["phone"] is None
    assert "updated_at" in upgraded

    result = vm.validate_schema(upgraded)
    assert result["valid"] is True
