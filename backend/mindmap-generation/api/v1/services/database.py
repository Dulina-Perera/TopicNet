# %%
import re
from sqlalchemy.orm.session import Session

from .exceptions import InvalidURIError
from .verification_n_validation import does_s3_file_exist
from ..models import Document, SessionLocal

# %%
def store_s3_file_uri(file_uri: str) -> bool:
  # Verify that the file URI is valid.
  if file_uri is None:
    raise InvalidURIError("The file URI is empty.")
  elif not re.match(r"https://\w+\.s3\.\w+-\w+-\d+\.amazonaws\.com/\w+", file_uri):
    raise InvalidURIError("The file URI is invalid.")

  # Check if the s3 file pointed to by the file URI exists.
  does_s3_file_exist(file_uri, "topicnet")

	# Create a new session.
  session: Session = SessionLocal()

  try:
    # Create a new document object.
    document: Document = Document(path=file_uri)

    # Add the document to the session and commit the transaction.
    session.add(document)
    session.commit()

    return True
  except Exception:
    # Rollback the transaction if an error occurs.
    session.rollback()

    return False
  finally:
    # Close the session.
    session.close()
