from pydantic import BaseModel, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

env_path = Path(__file__).parent.parent.resolve() / '.env'


class App(BaseModel):
    host: str
    port: int

class LoginProxy(BaseModel):
    url: AnyHttpUrl

class JWT(BaseModel):
    private_key: str | None = None
    public_key: str | None = None
    algorithm: str

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_path, env_nested_delimiter='__')

    app: App
    login_proxy: LoginProxy
    jwt: JWT

conf = Settings()
