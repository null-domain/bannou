import pathlib
import typing

import yaml

try:
    from yaml import CLoader as YamlLoader
except ImportError:
    from yaml import YamlLoader


class Secret:
    __slots__: typing.Sequence[str] = ("_secret_value",)

    def __init__(self, value: str):
        self._secret_value = value

    def __repr__(self):
        return "Secret(******)"

    def __str__(self) -> str:
        return "******"

    def get_secret_value(self) -> str:
        return self._secret_value


class Service:
    __slots__: typing.Sequence[str] = (
        "_protocol",
        "_driver",
        "_user",
        "_password",
        "_host",
        "_port",
        "_path",
    )

    def __init__(
        self,
        protocol: str,
        driver: str | None,
        user: str | None,
        password: str | None,
        host: str,
        port: int,
        path: str = "",
    ):
        """Generate a DSN string for a connection to an external service.

        Parameters
        ----------
        protocol : str
            The schema of the connection, for example, "postgresql", "mysql", "redis" etc.
        driver : str, optional
            The driver for the connection, for example, "asyncpg", "aiomysql" etc. Can be omitted.
        user : str, optional
            The username for the connection.
        password : str, optional
            The password for the connection.
        host : str
            The host for the connection.
        port : int
            The port for the connection.
        path : str, optional
            The path to use for the connection, for example, the database name for a database connection.
            Can be omitted.
        """
        self._protocol = protocol
        self._driver = driver
        self._user = user
        self._password = Secret(password) if password else None
        self._host = host
        self._port = port
        self._path = path

    @classmethod
    def from_settings_maker(
        cls, *, protocol: str, driver: str
    ) -> typing.Callable[[dict[str, typing.Any]], typing.Self]:
        def maker(settings: dict[str, typing.Any]) -> typing.Self:
            return cls(protocol=protocol, driver=driver, **settings)

        return maker

    @property
    def user(self) -> str | None:
        return self._user

    @property
    def password(self) -> Secret | None:
        return self._password

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def path(self) -> str:
        return self._path

    def __repr__(self):
        return (
            "DSN("
            f"protocol={self._protocol}, "
            f"driver={self._driver}, "
            f"user={self.user}, "
            f"password={self.password}, "
            f"host={self.host}, "
            f"port={self.port}, "
            f"path={self.path}"
            ")"
        )

    def __str__(self) -> str:
        return (
            f"{self._protocol}"
            f"{'+' + self._driver if self._driver else ''}"
            f"://{self.user if self.user else ''}{':' + str(self.password) if self.password else ''}"
            f"@{self.host}"
            f":{self.port}"
            f"/{self.path or ''}"
        )

    def build_url(self) -> str:
        return (
            f"{self._protocol}"
            f"{'+' + self._driver if self._driver else ''}"
            f"://{self.user if self.user else ''}{':' + self.password.get_secret_value() if self.password else ''}"
            f"{'@' if self.user or self.password else ''}{self.host}"
            f":{self.port}"
            f"/{self.path or ''}"
        )


_SENTINEL = ...


class BotSettings:
    __slots__: typing.Sequence[str] = ("bot_token", "logging", "postgres")

    bot_token: Secret
    logging: dict[str, typing.Any]
    postgres: Service

    def __init__(self, path: str) -> None:
        raw_config = pathlib.Path(path).expanduser().read_text()
        config = yaml.safe_load(raw_config)

        self._store_config_value("bot_token", config, cast=Secret)
        self._store_config_value("logging", config, default="INFO")
        self._store_config_value(
            "services:postgres",
            config,
            cast=Service.from_settings_maker(protocol="postgresql", driver="asyncpg"),
        )

    def _store_config_value(
        self,
        name: str,
        config: dict[str, typing.Any],
        *,
        default: typing.Any = _SENTINEL,
        cast: typing.Callable[[typing.Any], typing.Any] = None,
    ) -> typing.Any:
        keys = name.split(":")

        try:
            value = config
            for key in keys:
                value = value[key]
        except KeyError as ex:
            if default is _SENTINEL:
                raise RuntimeError(f"Missing {name!r} key in configuration") from ex

            value = default

        if cast:
            value = cast(value)

        object.__setattr__(self, keys[-1], value)

    def __setattr__(self, key, value):
        raise RuntimeError("Cannot set configuration values")


bot_settings = BotSettings("config.yaml")
"""Stores settings to be used for the bot and various other aspects of it.

This variable is a 'global state' object, and can be imported where necessary."""
