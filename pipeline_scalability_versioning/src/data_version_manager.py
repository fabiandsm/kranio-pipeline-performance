from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Optional, Tuple, Type


class DataVersionManager:
    """Gestor de versionado de datos y esquemas (demo para GitHub)."""

    def __init__(self):
        self.schemas = self._load_schemas()

    def _load_schemas(self) -> Dict[int, Dict[str, Any]]:
        """Cargar definiciones de esquemas por versión."""
        # Permitimos None en campos "nuevos" (email/phone) para compatibilidad retro.
        optional_str: Tuple[Type, ...] = (str, type(None))

        return {
            1: {
                "fields": ["id", "name", "created_at"],
                "types": {"id": str, "name": str, "created_at": str},
            },
            2: {
                "fields": ["id", "name", "email", "created_at", "updated_at"],
                "types": {
                    "id": str,
                    "name": str,
                    "email": optional_str,        # <- cambio mínimo
                    "created_at": str,
                    "updated_at": str,
                },
            },
            3: {
                "fields": ["id", "name", "email", "phone", "created_at", "updated_at"],
                "types": {
                    "id": str,
                    "name": str,
                    "email": optional_str,        # <- cambio mínimo
                    "phone": optional_str,        # <- cambio mínimo
                    "created_at": str,
                    "updated_at": str,
                },
            },
        }

    def validate_schema(self, data: Dict[str, Any], version: Optional[int] = None) -> Dict[str, Any]:
        """Validar que datos cumplan esquema de versión específica."""
        if version is None:
            version = int(data.get("schema_version", 1))

        if version not in self.schemas:
            return {"valid": False, "error": f"Versión {version} no soportada", "version": version, "errors": []}

        schema = self.schemas[version]
        errors = []

        # Verificar campos requeridos
        for field in schema["fields"]:
            if field not in data:
                errors.append(f"Campo faltante: {field}")

        # Verificar tipos (permitimos tuple de tipos)
        for field, expected_type in schema["types"].items():
            if field in data:
                value = data[field]
                if not isinstance(value, expected_type):
                    # expected_type puede ser tuple
                    if isinstance(expected_type, tuple):
                        expected_name = " | ".join([t.__name__ for t in expected_type])
                    else:
                        expected_name = expected_type.__name__
                    errors.append(f"Tipo incorrecto para {field}: esperado {expected_name}")

        return {"valid": len(errors) == 0, "version": version, "errors": errors}

    def upgrade_data(self, data: Dict[str, Any], target_version: int) -> Dict[str, Any]:
        """Upgrade datos a versión más nueva (compatibilidad incremental)."""
        current_version = int(data.get("schema_version", 1))
        data = dict(data)  # evitar mutar entrada original

        while current_version < target_version:
            data = self._upgrade_one_version(data, current_version)
            current_version += 1
            data["schema_version"] = current_version

        return data

    def _upgrade_one_version(self, data: Dict[str, Any], from_version: int) -> Dict[str, Any]:
        """Upgrade de una versión a la siguiente."""
        data = dict(data)

        if from_version == 1:
            # V1 → V2: Agregar email y updated_at
            data["email"] = data.get("email", None)
            data["updated_at"] = data.get("updated_at", data.get("created_at"))
            data["schema_version"] = 2

        elif from_version == 2:
            # V2 → V3: Agregar phone
            data["phone"] = data.get("phone", None)
            data["schema_version"] = 3

        return data

    def create_migration_script(self, from_version: int, to_version: int) -> str:
        """Generar script de migración para base de datos (demo)."""
        migrations = {
            (1, 2): """
-- Migración V1 → V2
ALTER TABLE users ADD COLUMN email VARCHAR(255);
ALTER TABLE users ADD COLUMN updated_at TIMESTAMP;
UPDATE users SET updated_at = created_at WHERE updated_at IS NULL;
""".strip(),
            (2, 3): """
-- Migración V2 → V3
ALTER TABLE users ADD COLUMN phone VARCHAR(50);
""".strip(),
        }

        return migrations.get(
            (from_version, to_version),
            f"-- No migration script available for {from_version} → {to_version}",
        )


if __name__ == "__main__":
    version_manager = DataVersionManager()

    legacy_data = {
        "schema_version": 1,
        "id": "123",
        "name": "Juan Pérez",
        "created_at": "2024-01-01T10:00:00",
    }

    validation = version_manager.validate_schema(legacy_data)
    print(f"Datos válidos: {validation['valid']}")
    if not validation["valid"]:
        print(f"Errores: {validation['errors']}")

    upgraded_data = version_manager.upgrade_data(legacy_data, 3)
    print(f"Datos upgradeados a versión: {upgraded_data['schema_version']}")

    validation_upgraded = version_manager.validate_schema(upgraded_data)
    print(f"Datos upgradeados válidos: {validation_upgraded['valid']}")
