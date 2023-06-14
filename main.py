from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime,timedelta
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from cfg import CLIENT_ID,CLIENT_SECRET,SPOTIPY_REDIRECT_URI


scope = "user-read-recently-played"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

def extract(date,limit=50):
    """ Get limit elements from last listen tracks

    Args:
        ds (datetime): Date to query
        limit (int): Limit of element to query
    """
    ds = int(date.timestamp())*1000
    return sp.current_user_recently_played(limit=limit,after=ds)

def transform(raw_data,date):
    data = []
    for r in raw_data["items"]:
        data.append(
            {
                "played_at" : r["played_at"],
                "artist" : r["track"]["artist"][0],
                "track" : r["track"]["name"]
            }
        )
    df = pd.DataFrame(data)

    # remove dates different from what we want
    clean_df = df[pd.to_datetime(df["played_at"]).dt.date ==date.date()]

    # Data validation FTW
    if not df["played_at"].is_unique:
        raise Exception("A value from played_at is not unique")
    if df.isnull().values.any():
        raise Exception("A value in df is null")

    return clean_df

def load(df):
    print(f"Uploading {df.shape[0]} to pg")
    #engine = create_engine(DB_CONNSTR)
    #df.to_sql(TABLENAME, con=engine, index=False, if_exists='append')

if __name__ == "__main__":
    date = datetime.today() - timedelta(days=1)

    # Extract
    data_raw =extract(date)
    print(f"Extracted {(data_raw['items'])} registers")





