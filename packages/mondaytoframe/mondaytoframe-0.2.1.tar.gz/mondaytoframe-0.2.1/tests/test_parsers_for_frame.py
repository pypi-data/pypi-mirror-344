import pytest
import pandas as pd
from datetime import datetime
from mondaytoframe.parsers_for_frame import (
    parse_email_for_df,
    parse_date_for_df,
    parse_text_for_df,
    parse_link_for_df,
    parse_people_for_df,
    parse_status_for_df,
    parse_checkbox_for_df,
    parse_tags_for_df,
    parse_long_text_for_df,
    parse_phone_for_df,
    parse_dropdown_for_df,
    parse_numbers_for_df,
)
import numpy as np
from mondaytoframe.model import (
    CheckboxColumnValue,
    ColumnValue,
    DateColumnValue,
    DropdownColumnValue,
    LinkColumnValue,
    NumberColumnValue,
    PeopleColumnValue,
    PhoneColumnValue,
    TagsColumnValue,
)
from deepdiff import DeepDiff


@pytest.mark.parametrize(
    "func,input_value,expected",
    [
        (
            parse_email_for_df,
            ColumnValue(id="1", text="test@example.com", type="email", value=None),
            "test@example.com",
        ),
        (
            parse_email_for_df,
            ColumnValue(id="1", text="", type="email", value=None),
            None,
        ),
        (
            parse_date_for_df,
            DateColumnValue(
                id="1", text="2025-02-10", type="date", value='{"date": "2025-02-10"}'
            ),
            datetime(2025, 2, 10, 0, 0),
        ),
        (
            parse_date_for_df,
            DateColumnValue(id="1", text="", type="date", value=None),
            pd.NaT,
        ),
        (
            parse_date_for_df,
            DateColumnValue(
                id="1",
                text="",
                type="date",
                value='{"date":"2025-02-10", "time": null}',
            ),
            datetime(2025, 2, 10, 0, 0),
        ),
        (
            parse_date_for_df,
            DateColumnValue(
                id="1",
                text="",
                type="date",
                value='{"date":null, "time": null}',
            ),
            pd.NaT,
        ),
        (
            parse_text_for_df,
            ColumnValue(id="1", text="some text", type="text", value=None),
            "some text",
        ),
        (
            parse_text_for_df,
            ColumnValue(id="1", text="", type="text", value=None),
            None,
        ),
        (
            parse_link_for_df,
            LinkColumnValue(
                id="1",
                text="https://example.com",
                type="link",
                value='{"text": "https://example.com", "url": "https://example.com"}',
            ),
            "https://example.com",
        ),
        (
            parse_link_for_df,
            LinkColumnValue(id="1", text="", type="link", value=None),
            None,
        ),
        (
            parse_people_for_df,
            PeopleColumnValue(
                id="1",
                text="John Doe",
                type="people",
                value='{"personsAndTeams": [{"id": 1, "kind": "person"}]}',
            ),
            "1",
        ),
        (
            parse_people_for_df,
            PeopleColumnValue(id="1", text="", type="people", value=None),
            None,
        ),
        (
            parse_status_for_df,
            ColumnValue(id="1", text="Working on it", type="status", value=None),
            "Working on it",
        ),
        (
            parse_status_for_df,
            ColumnValue(id="1", text="", type="status", value=None),
            "",
        ),
        (
            parse_checkbox_for_df,
            CheckboxColumnValue(id="1", text="v", type="checkbox"),
            True,
        ),
        (
            parse_checkbox_for_df,
            CheckboxColumnValue(id="1", text="", type="checkbox"),
            False,
        ),
        (
            parse_tags_for_df,
            TagsColumnValue(
                id="1",
                text="tag1, tag2",
                type="tags",
                tags=[{"name": "tag1"}, {"name": "tag2"}],
            ),
            {"tag1", "tag2"},
        ),
        (
            parse_tags_for_df,
            TagsColumnValue(id="1", text="", type="tags", tags=[]),
            set(),
        ),
        (
            parse_long_text_for_df,
            ColumnValue(id="1", text="long text", type="long_text", value=None),
            "long text",
        ),
        (
            parse_long_text_for_df,
            ColumnValue(id="1", text="", type="long_text", value=None),
            None,
        ),
        (
            parse_phone_for_df,
            PhoneColumnValue(
                id="1",
                text="31622222222",
                type="phone",
                value='{"phone": "31622222222", "countryShortName": "NL"}',
            ),
            "+31622222222 NL",
        ),
        (
            parse_phone_for_df,
            PhoneColumnValue(id="1", text="", type="phone", value=None),
            None,
        ),
        (
            parse_dropdown_for_df,
            DropdownColumnValue(
                id="1", type="dropdown", values=[{"label": "a,"}, {"label": "b,"}]
            ),
            {"a,", "b,"},
        ),
        (
            parse_dropdown_for_df,
            DropdownColumnValue(id="1", type="dropdown", values=[]),
            set(),
        ),
        (
            parse_numbers_for_df,
            NumberColumnValue(id="1", text="10.0", type="numbers", value=None),
            10.0,
        ),
        (
            parse_numbers_for_df,
            NumberColumnValue(id="1", text="", type="numbers", value=None),
            np.nan,
        ),
    ],
)
def test_parsers_for_df(func, input_value, expected):
    assert not DeepDiff(func(input_value), expected, ignore_nan_inequality=True)
