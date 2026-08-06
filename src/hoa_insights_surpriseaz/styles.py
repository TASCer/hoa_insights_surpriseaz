def parcel_updates() -> list[dict]:
    web_styles_changes = [
        dict(
            selector="page",
            props=[("size", "A3"), ("margin", "2cm")],
        ),
        dict(
            selector="th",
            props=[
                ("color", "blue"),
                ("border", "1px solid #eee"),
                ("padding", "1px 2px"),
                ("font-size", "8px"),
            ],
        ),
        # dict(
        #     selector="td:nth-child(-n + 2)",
        #     props=[("color", "orange"), ("font-size", "21px")],
        # ),
        dict(selector="tr", props=[("color", "red"), ("font-size", "8px")]),
        dict(
            selector=" ",
            props=[
                ("font-family", "Arial"),
                ("text-align", "center"),
                ("margin", "3px auto"),
                ("border", "1px solid black"),
            ],
        ),
        dict(
            selector="caption",
            props=[("caption-side", "top"), ("font-size", "11px"), ("color", "blue")],
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
                ("background", "grey"),
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
            props=[("caption-side", "top"), ("font-size", "20px"), ("color", "blue")],
        ),
    ]

    return web_styles_finance
