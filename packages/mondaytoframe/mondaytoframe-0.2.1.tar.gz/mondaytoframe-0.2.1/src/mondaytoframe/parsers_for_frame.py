from datetime import datetime
from typing import Any

import pandas as pd
from mondaytoframe.model import (
    CheckboxColumnValue,
    ColumnType,
    DateColumnValue,
    ColumnValue,
    DropdownColumnValue,
    LinkColumnValue,
    NumberColumnValue,
    PeopleColumnValue,
    PhoneColumnValue,
    TagsColumnValue,
)


def parse_email_for_df(v: ColumnValue) -> Any:
    return v.text if v.text else None


def parse_date_for_df(v: DateColumnValue) -> Any:
    if v.value is None or v.value.date is None:
        return pd.NaT
    return datetime.combine(v.value.date, v.value.time)


def parse_text_for_df(v: ColumnValue):
    return v.text if v.text else None


def parse_link_for_df(v: LinkColumnValue):
    if v.value is None:
        return None
    return v.value.url


def parse_people_for_df(v: PeopleColumnValue):
    if v.value is None:
        return None
    return ",".join([v.id for v in v.value.personsAndTeams])


def parse_status_for_df(v: ColumnValue):
    return v.text


def parse_checkbox_for_df(v: CheckboxColumnValue) -> bool:
    return True if v.text else False


def parse_tags_for_df(v: TagsColumnValue):
    return set([v.name for v in v.tags])


def parse_long_text_for_df(v: ColumnValue):
    return v.text if v.text else None


def parse_phone_for_df(v: PhoneColumnValue):
    if v.value is None:
        return None
    return f"{v.value.phone} {v.value.countryShortName}"


def parse_dropdown_for_df(v: DropdownColumnValue):
    return set(v.label for v in v.values)


def parse_numbers_for_df(v: NumberColumnValue):
    return v.text


PARSERS_FOR_DF = {
    ColumnType.email: parse_email_for_df,
    ColumnType.date: parse_date_for_df,
    ColumnType.text: parse_text_for_df,
    ColumnType.link: parse_link_for_df,
    ColumnType.people: parse_people_for_df,
    ColumnType.status: parse_status_for_df,
    ColumnType.checkbox: parse_checkbox_for_df,
    ColumnType.tags: parse_tags_for_df,
    ColumnType.long_text: parse_long_text_for_df,
    ColumnType.phone: parse_phone_for_df,
    ColumnType.dropdown: parse_dropdown_for_df,
    ColumnType.numbers: parse_numbers_for_df,
}
