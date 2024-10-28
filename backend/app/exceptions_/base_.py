# %%
class EnvVarNotSetError(Exception):
  def __init__(self, env_var: str) -> None:
    super().__init__(f"Environment variable {env_var} not set.")

class EnvVarsNotSetError(Exception):
  def __init__(self) -> None:
    super().__init__("Environment variables not set.")
