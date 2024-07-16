class NoSentencesToEncodeError(Exception):
		def __init__(self, message: str = 'No sentences to encode') -> None:
			super().__init__(message)
