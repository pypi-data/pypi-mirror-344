import pandas as pd
from .db import Database
from .models import Device
from datetime import datetime

class DataUploader:
    """
    Service class to upload device records into the database from a Pandas DataFrame.

    Example usage:
        >>> db = Database(db_uri)
        >>> uploader = DataUploader(db)
        >>> uploader.upload_from_dataframe(df)
    """

    def __init__(self, db: Database):
        """
        Initialize the DataUploader with a database connection.

        Args:
            db (Database): Initialized Database object providing SQLAlchemy sessions.
        """
        self.db = db
        self.session = self.db.get_session()

    def upload_from_dataframe(self, df: pd.DataFrame) -> None:
        """
        Upload a Pandas DataFrame of devices into the PostgreSQL database.

        Args:
            df (pd.DataFrame): DataFrame containing device data matching the Device model schema.

        Raises:
            KeyError: If required columns are missing from the DataFrame.
            ValueError: If date fields are improperly formatted.
        """
        devices = []
        for _, row in df.iterrows():
            device = Device(
                device_name=row['device_name'],
                price=row['price'],
                model=row['model'],
                brand=row['brand'],
                serial_number=row['serial_number'],
                date=datetime.strptime(row['date'], "%Y-%m-%d").date(),
                brand_code=row['brand_code'],
                product_number=row['product_number']
            )
            devices.append(device)

        self.session.add_all(devices)
        self.session.commit()
