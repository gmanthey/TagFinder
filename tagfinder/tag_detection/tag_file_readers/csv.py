import pandas as pd

from tagfinder.tag import Tag


def csv(tag_file, **kwargs) -> "list[Tag]":
    db = pd.read_csv(tag_file)

    tags = []

    for _,row in db.iterrows():
        tags.append(Tag(row.mfgID, [row.param1, row.param2, row.param3], row.period))
        
    return tags