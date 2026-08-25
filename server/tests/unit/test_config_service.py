import pytest
from server.src.core.exceptions import ValidationError
from server.src.modules.system.config_service import ConfigService

def test_validate_and_sanitize_valid_config():
    valid_payload = {
        "threshold": 0.25,
        "adaptive_alpha_threshold": 20,
        "is_adaptive": False,
        "manual_alpha": 0.6
    }
    sanitized = ConfigService.validate_and_sanitize(valid_payload)
    assert sanitized["threshold"] == 0.25
    assert sanitized["adaptive_alpha_threshold"] == 20
    assert sanitized["is_adaptive"] is False
    assert sanitized["manual_alpha"] == 0.6

def test_validate_and_sanitize_discards_unknown_keys():
    payload_with_injection = {
        "manual_alpha": 0.5,
        "malicious_key": "some_payload",
        "secret_admin": True
    }
    sanitized = ConfigService.validate_and_sanitize(payload_with_injection)
    assert "malicious_key" not in sanitized
    assert "secret_admin" not in sanitized
    assert sanitized["manual_alpha"] == 0.5

def test_validate_and_sanitize_invalid_values():
    with pytest.raises(ValidationError):
        ConfigService.validate_and_sanitize({"manual_alpha": 1.5})  # > 1.0
        
    with pytest.raises(ValidationError):
        ConfigService.validate_and_sanitize({"threshold": -0.5})  # < 0.0
        
    with pytest.raises(ValidationError):
        ConfigService.validate_and_sanitize({"adaptive_alpha_threshold": 0})  # < 1
