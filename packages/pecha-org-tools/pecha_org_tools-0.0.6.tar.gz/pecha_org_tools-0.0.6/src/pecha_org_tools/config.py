import tempfile

import urllib3

spreedsheet_id = "16pvNdKqGSb_CNZEkzS8B9fn_o9MMsoqA4vC5_X9G7bc"
spreedsheet_link = (
    f"https://docs.google.com/spreadsheets/d/{spreedsheet_id}/export?format=xlsx"
)


def download_spreedsheet(spreedsheet_link: str = spreedsheet_link):
    # B.1 download the catalog
    http = urllib3.PoolManager()
    r = http.request("GET", spreedsheet_link, preload_content=False)
    tmp = tempfile.NamedTemporaryFile(mode="wb", suffix=".xlsx", delete=False)
    while True:
        data = r.read(65536)
        if not data:
            break
        tmp.write(data)
    r.release_conn()
    return tmp.name
