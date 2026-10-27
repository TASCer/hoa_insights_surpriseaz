# ruff: noqa: C408
def parcel_updates() -> list[dict]:
    web_styles_changes = [
        dict(
            selector="th:nth-child(2n+3)",
            props=[
                ("color", "green"),
                ("font-size", "7px"),
            ],
        ),
        dict(
            selector="th:nth-child(2n+2)",  # even
            props=[
                ("color", "red"),
                ("font-size", "7px"),
            ],
        ),
        dict(
            selector="th:nth-child(2)",  # even
            props=[
                ("color", "grey"),
                ("font-size", "7px"),
            ],
        ),
        dict(
            selector="td:nth-child(2n+3)",
            props=[("color", "green"), ("font-size", "6px")],
        ),
        dict(
            selector="td:nth-child(2n+2)",
            props=[("color", "red"), ("font-size", "6px")],
        ),
        dict(
            selector=" ",
            props=[
                ("font-family", "Arial"),
                ("text-align", "center"),
                ("margin", "auto"),
                ("border", "1px solid black"),
                ("font-size", "6px"),
                ("color", "#5a5151"),
            ],
        ),
        dict(
            selector="caption",
            props=[("caption-side", "top"), ("font-size", "8px"), ("color", "black")],
        ),
    ]

    return web_styles_changes


def finance_updates() -> list[dict]:
    web_styles_finance = [
        dict(
            selector="th",
            props=[
                ("color", "black"),
                ("border", "1px solid #eee"),
                ("padding", "6px 7px"),
                ("background", "#90ee90"),
                ("font-size", "18px"),
            ],
        ),
        dict(
            selector="td:last-child", props=[("color", "green"), ("font-size", "18px")]
        ),
        dict(
            selector=" ",
            props=[
                ("font-family", "Roboto"),
                ("text-align", "center"),
                ("margin", "20px auto"),
                ("border", "6px solid black"),
                ("table-layout", "fixed"),
                ("border-style", "ridge"),
            ],
        ),
        dict(
            selector="caption",
            props=[("caption-side", "top"), ("font-size", "14px"), ("color", "black")],
        ),
    ]

    return web_styles_finance
