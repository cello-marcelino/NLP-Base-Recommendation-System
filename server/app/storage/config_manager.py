import os
import json
from flask import current_app

class ConfigManager:
    @staticmethod
    def get_config():
        config_path = current_app.config['CONFIG_JSON_PATH']
        default_config = {
            "threshold": 0.0,
            "adaptive_alpha_threshold": 15,
            "is_adaptive": True,
            "manual_alpha": 0.7
        }
        
        if not os.path.exists(config_path):
            return default_config
            
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                return {**default_config, **config}
        except:
            return default_config
            
    @staticmethod
    def update_config(new_config):
        config_path = current_app.config['CONFIG_JSON_PATH']
        current = ConfigManager.get_config()
        
        updated = {**current, **new_config}
        
        with open(config_path, 'w') as f:
            json.dump(updated, f, indent=4)
            
        return updated
