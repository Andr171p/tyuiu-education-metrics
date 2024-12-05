import pandas as pd
from dataclasses import dataclass
from typing import List, Optional

from src.config import BASE_DIR


@dataclass
class UserEducation:
    file_path: str = BASE_DIR / "data" / "Бак 2019-2020.csv"
    feature: str = "Законченное образ. учреждение"

    def get_users_educations(self) -> List[Optional[str]]:
        df: pd.DataFrame = pd.read_csv(self.file_path)
        educations = df[self.feature].str.split('(', expand=True)[0]
        educations = educations.where(pd.notnull(educations), '')
        return educations.tolist()


print(UserEducation().get_users_educations())