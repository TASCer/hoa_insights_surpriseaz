def test_fetch_pdf(parse_pdf) -> list[dict]:
    assert len(parse_pdf) == 15

    # assert len(consumed_parcel_data) == 15


if __name__ == "__main__":
    print(test_fetch_pdf())