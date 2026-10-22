# ruff: noqa: C408
def parcel_updates() -> list[dict]:
    web_styles_changes = [
        dict(
            selector="page",
            props=[("size", "A3"), ("margin", "2cm")],
        ),
        # dict(
        #     selector="th:nth-child(2n+3)",  
        #     props=[
        #         ("color", "red"),
        #         ("border", "1px solid #eee"),
        #         ("padding", "1px 2px"),
        #         ("font-size", "16px"),
        #     ],
        # ),
        # dict(
        #     selector="th:nth-child(n+3)",   #even
        #     props=[
        #         ("color", "green"),
        #         ("border", "1px solid #eee"),
        #         ("padding", "1px 2px"),
        #         ("font-size", "16px"),
        #     ],
        # ),
        
        dict(
            selector="td:nth-child(2n+3)",
            props=[("color", "green"), ("font-size", "14px")],
        ),
        dict(selector="td:nth-child(2n+2)", props=[("color", "red"), ("font-size", "14px")]),
        dict(
            selector=" ",
            props=[
                ("font-family", "Arial"),
                ("text-align", "center"),
                ("margin", "2px auto"),
                ("border", "1px solid black"),
            ],
        ),
        dict(
            selector="caption",
            props=[("caption-side", "top"), ("font-size", "14px"), ("color", "black")],
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
