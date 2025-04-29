import pandas as pd
import pytest
from unittest.mock import MagicMock

from unified_parts_processor.uploader import DataUploader
from unified_parts_processor.models import Device

# Mock Database
class MockDatabase:
    def __init__(self):
        self.session = MagicMock()

    def get_session(self):
        return self.session

@pytest.fixture
def sample_dataframe():
    data = {
        "device_name": [
            "Office Printer Pro",
            "Network Switch 24P",
            "Security Camera HD",
            "Wireless Router AC",
        ],
        "price": [299.99, 199.5, 149.99, 89.99],
        "model": ["MP-2000", "NS-24G", "SC-1080P", "WR-AC1200"],
        "brand": ["HP", "Cisco", "Dahua", "TP-Link"],
        "serial_number": ["SN001", "SN002", "SN003", "SN004"],
        "date": ["2024-01-15", "2024-02-01", "2024-02-15", "2024-03-01"],
        "brand_code": ["50.0359", "52.6294", "51.4484", "50.3866"],
        "product_number": ["19.1784", "22.0481", "23.5935", "23.4464"],
    }
    return pd.DataFrame(data)

def test_upload_from_dataframe(sample_dataframe):
    mock_db = MockDatabase()
    uploader = DataUploader(mock_db)

    uploader.upload_from_dataframe(sample_dataframe)

    mock_db.session.add_all.assert_called_once()

    devices_added = mock_db.session.add_all.call_args[0][0]

    assert len(devices_added) == 4
    assert all(isinstance(device, Device) for device in devices_added)

    first_device = devices_added[0]
    assert first_device.device_name == "Office Printer Pro"
    assert first_device.price == 299.99
    assert first_device.model == "MP-2000"
    assert first_device.brand == "HP"
    assert first_device.serial_number == "SN001"
    assert first_device.brand_code == "50.0359"
    assert first_device.product_number == "19.1784"
