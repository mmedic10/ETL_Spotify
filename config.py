"""Configurations for whole project"""

import os
import ast
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseSettings
from typing import List

# find .env automagically by walking up directories until it's found, then
# load up the .env entries as environment variables
load_dotenv(find_dotenv())


class Settings(BaseSettings):
    """The main settings to use in this project"""

    # Settings Api Spotify
    CLIENT_ID = str
    CLIENT_SECRET = str
    SPOTIPY_REDIRECT_URI = str




    # Settings v1&v2 database (postgres)
    POSTGRES_USER: str
    POSTGRES_PASS: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str


    ISSUE_FIELDS: List[dict] = list()

    # Who is going to have privileges on the postgres views
    # VIEW_PRIVILEGES: list[str]

    @property
    def postgres_uri(self):
        """the url for the output db"""
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASS}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def postgres_uri_v2(self):
        """the postgres' url for the transactions v2 db"""
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER_V2}:{self.POSTGRES_PASS_V2}@"
            f"{self.POSTGRES_HOST_V2}:{self.POSTGRES_PORT_V2}/{self.POSTGRES_DB_V2}"
        )


    class Config:
        """Configurations of how the env variables are considered"""

        case_sensitive = True


settings = Settings()  # create an instance