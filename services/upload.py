import csv
import io
import magic

from exceptions import UploadValidationError

MAX_ROWS = 10000
MAX_COLS = 100
MAX_CELL_LENGTH = 1000

ALLOWED_MIMES = {
    "text/csv",
    "text/plain",
    "application/csv",
    "application/vnd.ms-excel",
}


def dangerous_cell(value):
    return (
        isinstance(value, str)
        and value.startswith(("=", "+", "-", "@"))
    )


def validate_csv_upload(file):

    if not file.filename.lower().endswith(".csv"):
        raise UploadValidationError(
            "Only CSV files are allowed"
        )

    header = file.stream.read(2048)
    file.stream.seek(0)

    mime = magic.from_buffer(header, mime=True)

    if mime not in ALLOWED_MIMES:
        raise UploadValidationError(
            "Invalid CSV file"
        )


def process_csv(file):

    validate_csv_upload(file)

    raw = file.stream.read()

    if not raw:
        raise UploadValidationError(
            "Empty file"
        )

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise UploadValidationError(
            "CSV must be UTF-8 encoded"
        )

    reader = csv.reader(io.StringIO(text))

    rows = []

    for row_num, row in enumerate(reader):

        if row_num > MAX_ROWS:
            raise UploadValidationError(
                "Too many rows"
            )

        if len(row) > MAX_COLS:
            raise UploadValidationError(
                "Too many columns"
            )

        clean_row = []

        for cell in row:

            if len(cell) > MAX_CELL_LENGTH:
                raise UploadValidationError(
                    "Cell too large"
                )

            if dangerous_cell(cell):
                raise UploadValidationError(
                    "Formula cells are not allowed"
                )

            clean_row.append(cell)

        rows.append(clean_row)

    return rows