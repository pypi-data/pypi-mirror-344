from os import path
from typing import Sequence, MutableSequence, MutableMapping, cast
from os import path
from re import compile, sub, escape, IGNORECASE
from textwrap import indent

from sqlcompose.core.include import Include
from sqlcompose.core.compat import fix_path, get_relative_path

REGEX_INCLUDE = compile(r"\$INCLUDE\(([^\)]+)\)", IGNORECASE)


def loads(sql: str) -> str:
    """Compose SQL

    Args:
        sql (str): The query text

    Returns:
        str: The composed query
    """
    return cast(str, compose(sql, "SQL", path.curdir, path.curdir))


def load(filename: str) -> str:
    """Compose SQL

    Args:
        filename (str): The path of the file containing the SQL

    Returns:
        str: The composed query
    """


    filename = fix_path(filename)

    if not path.isfile(filename):
        raise FileNotFoundError(filename)


    with open(filename, "r", encoding="utf-8") as file:
        return cast(str, compose(file.read(), filename, filename, path.dirname(filename)))


def compose(
    sql: str,
    name: str,
    file_path: str,
    root: str,
    level: int = 1,
    included: MutableSequence[str] | None = None,
    included1: MutableMapping[str, tuple[str, int]] | None = None
) -> str | None:

    file_path = fix_path(file_path)
    included = included or []
    included1 = included1 or {}
    includes: list[Include] = []
    parent = included[len(included)-2] if len(included) > 1 else None

    if name in included and included1[name][1] == level:
        #duplicate include at the same level - return none, to use the previously composed SQL
        return None
    elif name in included:
        raise Exception(f"Circular dependency detected: File \"{get_relative_path(file_path, root)}\" has already been already included")
    else:
        included.append(name)
        included1[name] = (file_path, level)

    index = 1

    for match in REGEX_INCLUDE.finditer(sql):
        file_path_inner = fix_path(path.join(path.dirname(file_path), match.group(1)))
        try:
            with open(file_path_inner, "r", encoding="utf-8") as file:
                composed = compose(file.read(), match.group(1), file_path_inner, root, level=level+1)
        except FileNotFoundError:
            if not parent is None:
                raise FileNotFoundError(f"Include failed: File \"{get_relative_path(file_path_inner, root)}\" which was referred to in \"{get_relative_path(parent, root)}\", was not found...")
            else:
                raise FileNotFoundError(f"Include failed: File \"{get_relative_path(file_path_inner, root)}\" was not found...")

        if composed is not None:
            includes.append(
                Include(
                    composed,
                    f"Q_{level}_{index}",
                    match.group(0),
                    match.group(1)
                )
            )
            index = index + 1

    for include in includes:
        sql = sub(escape(include.match), include.name, sql)

    return wrap_cte_sql(includes, sql, level, name)

def wrap_cte_sql(includes: Sequence[Include], sql: str, level: int, source: str) -> str:
    sql_output = ""
    indent_str = "  "

    if len(includes) > 0:
        for include in includes:
            sql_output = "WITH " if sql_output == "" else sql_output + ", "
            sql_output = f"{sql_output}{include.name} AS (\n{include.sql}\n)"

        sql_output = sql_output + ", Q_{0} AS (\n{1}\n)\nSELECT * FROM Q_{0}".format(level, indent("--{1}\n{0}".format(sql, source), indent_str)) #+ "\.format(level)
    else:
        sql_output = f"--{source}\n{sql}"

    return sql_output if level == 1 else indent(sql_output, indent_str)




