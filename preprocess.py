with open("first_init", "r") as conf:
    first_line = conf.readline()

if first_line == "true":
    try:
        from settings import DATA_PATH, ALEMBIC_INI
        from alembic import command
        from alembic.config import Config
        from db import pg_engine
        from models.tables import Product, Review
        import pandas as pd
        from sqlalchemy.orm import sessionmaker
        import os
        from sqlalchemy.engine.base import Engine

        class Deserializer:
            def __init__(self, csv_dir_path: str) -> None:
                self._csv_dir_path = csv_dir_path

            def _is_csv_file(self, filename: str) -> bool:
                return filename.endswith(".csv")

            def read_csv_files(self):
                files_list = os.listdir(self._csv_dir_path)
                csv_filter = filter(self._is_csv_file, files_list)
                self._csv_files = list(csv_filter)
                return self

            def make_dataframes(self) -> list[pd.DataFrame]:
                dataframes = {}
                for file in self._csv_files:
                    full_path = os.path.join(self._csv_dir_path, file)
                    file_name = file.split(".")[0]
                    dataframe = pd.read_csv(full_path)
                    dataframes[file_name] = dataframe
                return dataframes

        class Migration:
            def __init__(self, dataframes: dict[str, pd.DataFrame]) -> None:
                self._dataframes = dataframes

            def make(self, engine: Engine):

                for name, dataframe in self._dataframes.items():
                    session = sessionmaker(bind=engine)()
                    with session:
                        if name == "products":
                            for index, row in dataframe.iterrows():
                                instance = Product(asin=row["Asin"],
                                                   title=row["Title"])
                                print(instance)
                                session.add(instance)
                        elif name == "reviews":
                            for index, row in dataframe.iterrows():
                                instance = Review(asin=row["Asin"],
                                                  title=row["Title"],
                                                  review=row["Review"])
                                print(instance)
                                session.add(instance)
                        session.commit()

        current_directory = os.path.dirname(os.path.realpath(__file__))
        full_data_path = current_directory + DATA_PATH
        alembic_cfg = Config(ALEMBIC_INI)
        command.upgrade(alembic_cfg, "head")
        deser = Deserializer(full_data_path)
        dataframes = deser.read_csv_files().make_dataframes()
        migration = Migration(dataframes=dataframes)
        migration.make(engine=pg_engine)
    finally:
        with open("first_init", "w") as conf:
            conf.write("false")

del first_line
