from typing import Literal, Dict, Any

from pydantic import Field, BaseSettings, validator

from procaaso_log.enum import Level, Env, Format


def auto_format(env: Env) -> Format:
    if env is Env.DEV:
        return Format.CONSOLE

    return Format.JSON


Output = Literal["stdout", "stderr"]


def auto_output(env: Env) -> Output:
    if env is Env.DEV:
        return "stderr"

    return "stdout"


class Settings(BaseSettings):
    # Logging config settings
    #   Common
    env: Env = Field(Env.PROD)
    level: Level = Field(Level.WARNING)

    #   Uncommon
    output: Output = Field("stdout")
    format: Format = Field(Format.AUTO)
    root: str = Field("")
    root_level: Level = Field(Level.WARNING)

    class Config:
        env_prefix = "procaaso_log_"

    @validator("format")
    def valid_env_format(
        cls, v: Format, values: Dict[str, Any], **kwargs: Any
    ) -> Format:
        fmt = v
        env = values["env"]
        if fmt is Format.AUTO:
            fmt = auto_format(env)

        if env is Env.PROD and fmt is not Format.JSON:
            raise ValueError("'format' must be 'JSON' when 'env' is 'PROD'")

        return fmt

    @validator("output")
    def valid_env_output(
        cls, v: Output, values: Dict[str, Any], **kwargs: Any
    ) -> Output:
        out = v
        env = values["env"]
        if env is Env.PROD and out != "stdout":
            raise ValueError("'output' must be 'stdout' when 'env' is 'PROD'")

        return out
