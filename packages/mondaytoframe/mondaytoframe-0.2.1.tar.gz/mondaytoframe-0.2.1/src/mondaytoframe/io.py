import os
import pandas as pd
from mondaytoframe.model import (
    ColumnType,
    SchemaBoard,
    SchemaResponse,
    ItemsByBoardResponse,
    BoardKind,
)
from mondaytoframe.parsers_for_frame import PARSERS_FOR_DF

from monday import MondayClient


from typing import Any, Literal

from mondaytoframe.parsers_for_monday import PARSERS_FOR_MONDAY
import logging
from pydantic import Field, validate_call, ConfigDict
from typing_extensions import Annotated

logger = logging.getLogger(__name__)

TOKEN_NAME = "MONDAYTOFRAME_TOKEN"

TokenType = Annotated[str, Field(default=os.getenv(TOKEN_NAME), validate_default=True)]


def _fetch_schema_board(monday: MondayClient, board_id: str) -> SchemaBoard:
    query_result = monday.boards.fetch_boards_by_id(board_id)
    validated = SchemaResponse(**query_result)
    return validated.data.boards[0]


def _create_or_get_tag(monday: MondayClient, tag_name: str):
    query_result = monday.custom.execute_custom_query(
        f"""mutation {{ create_or_get_tag (tag_name: "{tag_name}") {{ id }} }}"""
    )
    return int(query_result["data"]["create_or_get_tag"]["id"])


def fetch_items_by_board_id(
    monday_client: MondayClient,
    board_id: str,
    cursor: str | None = None,
    limit: int = 25,
    query_params=None,
):
    """
    Fetch items from a Monday.com board using the GraphQL API.

    Args:
        monday_client: The Monday.com client instance
        board_id (str): The board's unique identifier
        cursor (str, optional): Pagination cursor for fetching next pages
        limit (int, optional): Number of items to fetch per page (max 500)
        query_params (dict, optional): Additional query parameters for filtering/sorting

    Returns:
        dict: The query result containing items and pagination info
    """
    limit = min(limit, 500)  # API limit is 500
    cursor_part = f'cursor: "{cursor}"' if cursor is not None else ""
    query_params_part = (
        f"query_params: {query_params}" if query_params is not None else ""
    )

    query = f"""query {{
        boards(ids: ["{board_id}"]) {{
            items_page({cursor_part}, limit: {limit}, {query_params_part}) {{
                cursor
                items {{
                    id
                    name
                    group {{
                        id
                        title
                    }}
                    column_values {{
                        id
                        text
                        value
                        type
                        ... on DropdownValue {{
                            values {{
                                label
                            }}
                        }}
                        ... on TagsValue {{
                            tags {{
                                name
                            }}
                        }}
                    }}
                }}
            }}
        }}
    }}"""

    return monday_client.custom.execute_custom_query(query)


@validate_call(
    config=ConfigDict(arbitrary_types_allowed=True, coerce_numbers_to_str=True)
)
def read(
    board_id: str,
    monday_token: TokenType,
    unknown_type: Literal["text", "drop", "raise"] = "text",
    **kwargs: Any,
):
    """
    Read data from a Monday.com board into a pandas DataFrame.

    Arguments:
        board_id (str): The ID of the Monday.com board to read data from.
        monday_token (TokenType): The authentication token for Monday.com API.
        unknown_type (Literal["text", "drop", "raise"]): Specifies how to handle unknown column types.
            - "text": Use a default text parser for unknown column types (default).
            - "drop": Ignore unknown column types.
            - "raise": Raise a ValueError if unknown column types are found.
        **kwargs (dict[str, Any]): Additional arguments to pass to the Monday.com API.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the board data.

    Raises:
        ValueError: If unknown column types are found and `unknown_type` is set to "raise".

    Notes:
        The function uses predefined parsers for known column types. If a column type is not recognized and `unknown_type`
        is set to "text", a default text parser will be used. If `unknown_type` is set to "drop", the unknown columns will
        be ignored.

    Usage:

    ```python
    from mondaytoframe import read

    df = read(board_id="123456", monday_token="your_token")
    print(df.head())
    ```
    """
    monday = MondayClient(monday_token)
    column_specifications = _fetch_schema_board(monday, board_id).columns

    cols_without_parsers = {
        spec.id: spec.type
        for spec in column_specifications
        if spec.type not in PARSERS_FOR_DF and spec.id != "name"
    }
    col_parser_mapping = {
        spec.id: PARSERS_FOR_DF[spec.type]
        for spec in column_specifications
        if spec.type in PARSERS_FOR_DF
    }
    if cols_without_parsers:
        match unknown_type:
            case "raise":
                raise ValueError(
                    f"Unknown column types found in the board: {cols_without_parsers}."
                    "Set unknown_type='text' to try to get them using a default parser or "
                    "set unknown_type='drop' to ignore them."
                )
            case "drop":
                msg = (
                    f"Unknown column types found in the board: {cols_without_parsers}. Not reading them."
                    "Set unknown_type='text' to try to get them using a default text parser."
                )
                logger.warning(msg)
            case "text":
                col_parser_mapping.update(
                    {
                        col: PARSERS_FOR_DF[ColumnType.text]
                        for col in cols_without_parsers
                    }
                )

    items = []
    cursor = None
    while True:
        query_result = fetch_items_by_board_id(
            monday, board_id, cursor=cursor, **kwargs
        )
        validated = ItemsByBoardResponse(**query_result)
        board = validated.data.boards[0]
        items += board.items_page.items
        cursor = board.items_page.cursor
        if cursor is None:
            break

    items_parsed = []
    for item in items:
        column_values_dict = {
            (column_value.id): col_parser_mapping[column_value.id](column_value)  # type: ignore[operator]
            for column_value in item.column_values
            if column_value.id not in cols_without_parsers
        }

        record = {
            "id": item.id,
            "Name": item.name,
            "Group": item.group.title,
            **column_values_dict,
        }
        items_parsed.append(record)

    name_mapping = {
        spec.id: spec.title for spec in column_specifications if spec.title != "Name"
    }
    logger.info(
        f"Fetched {len(items_parsed)} items from board {board_id} with columns: {name_mapping}"
    )
    return pd.DataFrame.from_records(items_parsed, index="id").rename(
        columns=name_mapping
    )


def _align_df_with_board_schema(
    df: pd.DataFrame, monday: MondayClient, board_id: str, unknown_type: str
) -> pd.DataFrame:
    board_schema = _fetch_schema_board(monday, board_id)
    column_specifications = board_schema.columns
    tag_specifications = board_schema.tags

    # Check if all columns in the dataframe are in the board schema
    cols_without_parsers = []
    col_parser_mapping = {}
    for column in df.columns:
        if column in ["Name", "Group"]:
            col_parser_mapping[column] = PARSERS_FOR_MONDAY[ColumnType.text]
            continue

        col_spec = [spec for spec in column_specifications if spec.title == column]
        if not col_spec or col_spec[0].type not in PARSERS_FOR_MONDAY:
            cols_without_parsers.append(column)
        else:
            col_parser_mapping[column] = PARSERS_FOR_MONDAY[col_spec[0].type]

    if cols_without_parsers:
        match unknown_type:
            case "raise":
                raise ValueError(
                    f"Unknown column types found in the dataframe: {cols_without_parsers}."
                    "Set unknown_type='drop' to ignore this error and update all other columns."
                )
            case "drop":
                msg = f"Unknown column types found in the dataframe: {cols_without_parsers}. They will be ignored."
                logger.warning(msg)

    # Convert tags names to ids. Create new ids for tags that do not exist yet
    tag_mapping = {tag.name: tag.id for tag in tag_specifications}
    cols_with_tags = [
        spec.title
        for spec in column_specifications
        if spec.type == ColumnType.tags and spec.title in df.columns
    ]
    if cols_with_tags:
        tags_in_board = set(
            df[cols_with_tags]
            .apply(lambda s: s.explode().dropna().unique(), axis=1)
            .explode()
            .dropna()
        )
        missing_tag_mapping = {
            tag: _create_or_get_tag(monday, tag)
            for tag in tags_in_board - tag_mapping.keys()
        }
        all_tag_mapping = tag_mapping | missing_tag_mapping

        df = df.assign(
            **{
                col: df[col].map(
                    lambda ls: [all_tag_mapping[tag] for tag in ls] if ls else None
                )
                for col in cols_with_tags
            }
        )

    name_mapping = {spec.title: spec.id for spec in column_specifications}
    df = (
        df[list(col_parser_mapping)]
        .apply(lambda s: s.apply(col_parser_mapping[s.name]))
        .rename(columns=name_mapping)
    )
    return df


@validate_call(
    config=ConfigDict(arbitrary_types_allowed=True, coerce_numbers_to_str=True)
)
def update(
    board_id: str,
    df: pd.DataFrame,
    monday_token: TokenType,
    unknown_type: Literal["drop", "raise"] = "raise",
    **kwargs: Any,
):
    """
    Update a pandas DataFrame to a Monday.com board.

    Arguments:
        board_id (str): The ID of the Monday.com board.
        df (pd.DataFrame): The DataFrame to update to the board.
        monday_token (TokenType): The authentication token for Monday.com.
        unknown_type (Literal["drop", "raise"]): Specifies how to handle columns in the DataFrame that do not have a corresponding parser in the board schema.
            - "drop": Ignore columns that do not have a corresponding parser (default).
            - "raise": Raise a ValueError if columns do not have a corresponding parser.
        **kwargs (Any): Additional keyword arguments to pass to the Monday.com API.

    Raises:
        ValueError: If unknown_type is "raise" and there are columns in the DataFrame that do not have a corresponding parser in the board schema.

    Usage:

    ```python
    from mondaytoframe import update
    import pandas as pd

    df = pd.DataFrame({
        "Name": ["Task 1", "Task 2"],
        "Status": ["Done", "In Progress"],
        "Tags": [["tag1"], ["tag2", "tag3"]],
    })
    update(board_id="123456", df=df, monday_token="your_token")
    ```
    """

    if df.empty:
        return
    monday = MondayClient(monday_token)

    df = _align_df_with_board_schema(df, monday, board_id, unknown_type)

    for item_id, row in df.iterrows():
        monday.items.change_multiple_column_values(
            board_id=board_id,
            item_id=item_id,
            column_values=row.drop("Group").to_dict(),
            **kwargs,
        )
    logger.info(f"Items updated successfully on board {board_id}.")


@validate_call(
    config=ConfigDict(arbitrary_types_allowed=True, coerce_numbers_to_str=True)
)
def create_board(
    column_types: dict[str, ColumnType],
    monday_token: TokenType,
    board_name: str = "Created by mondaytoframe",
    board_kind: BoardKind = BoardKind.public,
    workspace_id: int | None = None,
) -> str:
    monday = MondayClient(monday_token)

    board = monday.boards.create_board(board_name, board_kind, workspace_id)
    board_id = board["data"]["create_board"]["id"]

    for title, col_type in column_types.items():
        monday.columns.create_column(
            board_id=board_id, column_title=title, column_type=col_type
        )
    logger.info(f"Board {board_id} created successfully.")

    return board_id


@validate_call(
    config=ConfigDict(arbitrary_types_allowed=True, coerce_numbers_to_str=True)
)
def create_items(
    board_id: str,
    df: pd.DataFrame,
    monday_token: TokenType,
    unknown_type: Literal["drop", "raise"] = "raise",
):
    """
    Creates items on a Monday.com board based on the provided dataframe.

    Args:
        board_id (str): The ID of the Monday.com board where items will be created.
        df (pd.DataFrame): A pandas DataFrame containing the data for the items to be created.
            The DataFrame must include a 'Name' column, and it must not contain null values.
        monday_token (TokenType): The authentication token for accessing the Monday.com API.
        unknown_type (Literal["drop", "raise"], optional): Specifies how to handle unknown columns
            in the DataFrame that do not match the board schema. Defaults to "raise".
            - "drop": Drops unknown columns.
            - "raise": Raises an error if unknown columns are found.

    Raises:
        ValueError: If the DataFrame is empty, does not contain a 'Name' column, or if the 'Name'
            column contains null values.

    Notes:
        - The function aligns the DataFrame with the board schema before creating items.
        - Each row in the DataFrame corresponds to an item on the board.
        - The 'name' and 'group' columns in the DataFrame are used for item names and group IDs,
          respectively. Other columns are treated as column values for the items.
    """
    if df.empty:
        return

    if "Name" not in df.columns:
        raise ValueError(
            "The dataframe must contain a 'Name' column to create items in Monday.com."
        )
    if df["Name"].isnull().any():
        raise ValueError(
            "The 'Name' column in the dataframe must not contain null values."
        )

    monday = MondayClient(monday_token)

    df = _align_df_with_board_schema(df, monday, board_id, unknown_type)

    for _, row in df.iterrows():
        monday.items.create_item(
            board_id=board_id,
            item_name=row["name"] if "name" in row else "",
            group_id=row["group"] if "group" in row else "",
            column_values=row.drop(["name", "group"], errors="ignore").to_dict(),
        )
    logger.info(f"Items created successfully on board {board_id}.")


@validate_call(
    config=ConfigDict(arbitrary_types_allowed=True, coerce_numbers_to_str=True)
)
def delete_board(
    board_id: str,
    monday_token: TokenType,
):
    """
    Delete a board in Monday.com.

    Arguments:
        board_id (str): The ID of the board to delete.
        monday_token (TokenType): The authentication token for Monday.com.

    Usage:

    ```python
    from mondaytoframe import delete_board

    delete_board(board_id="123456", monday_token="your_token")
    ```
    """
    monday = MondayClient(monday_token)
    monday.custom.execute_custom_query(
        f"mutation {{ delete_board (board_id: {board_id}) {{ id }} }}"
    )
    logger.info(f"Board {board_id} deleted successfully.")
