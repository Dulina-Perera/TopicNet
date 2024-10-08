# %%
from sqlalchemy.orm.session import Session
from time import sleep
from typing import Any

from .v_and_v import does_s3_file_exist, is_s3_uri_valid
from ....exceptions import InvalidS3URIError
from ....models import Document

# %%
def save_s3_uri(
	s3_uri: str,
	db_session: Session,
	s3_client: Any,
	max_retries: int = 3,
	retry_delay: int = 0.1
) -> int:

  # Verify that the S3 URI is valid.
  if not is_s3_uri_valid(s3_uri):
    raise InvalidS3URIError("The S3 URI is invalid.")

  # Check if the S3 file pointed to by the S3 URI exists.
  does_s3_file_exist(s3_uri, s3_client)

  retries: int = 0
  while retries < max_retries:
    try:
      # Create a new document object.
      document: Document = Document(path=s3_uri)

      # Add the document to the session and commit the transaction.
      db_session.add(document)
      db_session.commit()

      return document.id
    except Exception:
      # Rollback the transaction if an error occurs.
      db_session.rollback()

      # Increment the number of retries and wait before retrying.
      retries += 1
      sleep(retry_delay)
    finally:
      # Close the session only after all retries have been exhausted or a success.
      if retries == max_retries:
        db_session.close()

  # If the retries are exhausted, raise an exception.
  raise Exception("An error occurred while storing the S3 URI in the database.")
