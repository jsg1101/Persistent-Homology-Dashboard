import csv
import io
import magic
import html

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

    flagged_rows = []

    missing_count = 0
    invalid_count = 0

    for row_num, row in enumerate(reader):

        if row_num >= MAX_ROWS:
            raise UploadValidationError(
                "Too many rows"
            )

        if len(row) > MAX_COLS:
            raise UploadValidationError(
                "Too many columns"
            )

        flagged_row = []

        for cell in row:

            # Normalize
            if cell is None:
                cell = ""

            # Remove surrounding whitespace
            cell = str(cell).strip()

            # Cell size limit
            if len(cell) > MAX_CELL_LENGTH:
                raise UploadValidationError(
                    "Cell too large"
                )

            # Prevent formula injection
            if dangerous_cell(cell):
                raise UploadValidationError(
                    "Formula cells are not allowed"
                )

            # Prevent HTML injection
            safe_cell = sanitize_html(cell)

            ###########################################
            # CLASSIFICATION
            ###########################################

            # Missing
            if (
                safe_cell == ""
                or safe_cell.lower() == "nan"
                or safe_cell.lower() == "null"
            ):

                missing_count += 1

                flagged_row.append({
                    "value": safe_cell,
                    "type": "missing"
                })

            else:

                # Valid float?
                try:
                    float(safe_cell)

                    flagged_row.append({
                        "value": safe_cell,
                        "type": "normal"
                    })

                except ValueError:

                    invalid_count += 1

                    flagged_row.append({
                        "value": safe_cell,
                        "type": "invalid"
                    })

        flagged_rows.append(flagged_row)

    return {
        "data": flagged_rows,
        "missing": missing_count,
        "invalid": invalid_count,
        "total_issues": missing_count + invalid_count,
        "rows": len(flagged_rows),
        "cols": len(flagged_rows[0]) if flagged_rows else 0
    }


# Helper functions
def dangerous_cell(value):

    if not isinstance(value, str):
        return False

    trimmed = value.lstrip()

    return trimmed.startswith(("=", "+", "-", "@"))


def validate_csv_upload(file):

    if not file.filename.lower().endswith(".csv"):
        raise UploadValidationError(
            "Only CSV files are allowed"
        )

    header = file.stream.read(2048)
    file.stream.seek(0)

    mime = magic.from_buffer(header, mime=True)
    print(mime)

    if mime not in ALLOWED_MIMES:
        raise UploadValidationError(
            "Invalid CSV file"
        )
    
def sanitize_html(value):

    return html.escape(value)