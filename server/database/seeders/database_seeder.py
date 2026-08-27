import os
import json
from typing import Dict, Any

from server.src.config.config import Config
from server.src.config.logging_config import logger
from server.src.services.system.config_service import ConfigService

class DatabaseSeeder:
    """
    Seeds initial reference / static data (default runtime config, default roles).
    Follows rules/database.md: Seeder is for initial static reference data.
    """
    
    @staticmethod
    def seed_default_config():
        config_path = Config.CONFIG_JSON_PATH
        if not os.path.exists(config_path):
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(ConfigService.DEFAULT_CONFIG, f, indent=4)
            logger.info(f"Seeder: Default system config berhasil diinisialisasi ke {config_path}")
        else:
            logger.info("Seeder: System config sudah ada, melewati pembuatan ulang.")

    @classmethod
    def run(cls):
        logger.info("Menjalankan DatabaseSeeder...")
        cls.seed_default_config()
        logger.info("[OK] DatabaseSeeder selesai dijalankan.")

if __name__ == '__main__':
    DatabaseSeeder.run()
