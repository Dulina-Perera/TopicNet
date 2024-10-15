# %%
class EnvVarsNotSetError(Exception):
  def __init__(self) -> None:
    super().__init__("Environment variables not set")
