import json
import logging
import os
import sqlite3

from mcp.server.fastmcp import FastMCP
from sdif_db import SDIFDatabase

from sdif_mcp.prompt import CREATE_TRANSFORMATION

mcp = FastMCP("sdif")

logger = logging.getLogger(__name__)


@mcp.prompt()
async def create_transformation(
    input_file: str,
    input_schema: str,
    input_sample: str,
    output_files: str,
    output_schema: str,
    output_sample: str,
    output_representation: str,
):
    return CREATE_TRANSFORMATION.format(
        input_file=input_file,
        input_schema=input_schema,
        input_sample=input_sample,
        output_files=output_files,
        output_schema=output_schema,
        output_sample=output_sample,
        output_representation=output_representation,
    )


@mcp.resource(uri="schema://{sqlite_file}")
async def get_schema(sqlite_file: str) -> str:
    """
    Get the schema of a SQLite database.

    Args:
        sqlite_file: Path to the SQLite file

    Returns:
        String representation of the database schema
    """
    if not os.path.exists(sqlite_file):
        return f"Error: SQLite file {sqlite_file} not found or not authorized"

    try:
        with SDIFDatabase(sqlite_file, read_only=True) as db:
            schema_info = db.get_schema()

        return schema_info

    except sqlite3.Error as e:
        return f"Error getting schema: {str(e)}"


@mcp.resource(uri="sample://{sqlite_file}")
async def get_sample(sqlite_file: str) -> str:
    """Get the sample of a SQLite database."""
    if not os.path.exists(sqlite_file):
        return f"Error: SQLite file {sqlite_file} not found or not authorized"

    try:
        with SDIFDatabase(sqlite_file, read_only=True) as db:
            sample_analysis = db.get_sample_analysis(
                num_sample_rows=5,
                top_n_common_values=10,
            )
    except sqlite3.Error as e:
        return f"Error getting sample: {str(e)}"

    return sample_analysis


@mcp.tool()
async def execute_sql(sqlite_file: str, query: str) -> str:
    """
    Execute SQL query on a SQLite database.

    Args:
        sqlite_file: Path to the SQLite file
        query: SQL query to execute

    Returns:
        Results of the query as a formatted string
    """
    # Validate the file exists and is in our allowed list
    if not os.path.exists(sqlite_file):
        return f"Error: SQLite file {sqlite_file} not found or not authorized"

    try:
        with SDIFDatabase(sqlite_file, read_only=True) as db:
            result = db.query(query, return_format="dict")
            MAX_RESULTS = 50
            if len(result) > MAX_RESULTS:
                return json.dumps(
                    {
                        "data": result[:MAX_RESULTS],
                        "truncated": True,
                        "total_rows": len(result),
                    }
                )
            else:
                return json.dumps({"data": result, "truncated": False})
    except PermissionError as e:
        return f"Error: Query refused. {e}"
    except sqlite3.Error as e:
        return f"Error executing query: {e}"
    except Exception as e:
        logger.exception("Unexpected error in execute_sql tool")
        return f"Unexpected Error: {e}"


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
