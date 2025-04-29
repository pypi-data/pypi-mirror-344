import re

from abc import ABC, abstractmethod
from typing import Optional, Union, TypeVar, List, Any

from deprecated import deprecated
from pydantic import BaseModel, Field, model_validator

from .utils import ConnectionTypes


connectionType = TypeVar("connectionType", ConnectionTypes, str, None)


@deprecated(version="0.2.0", reason="Use EndpointMeta instead")
class HostMeta(BaseModel):
    host: Optional[str] = Field("localhost", description="Connection host")
    port: Optional[int] = Field(8000, description="Connection port")


class EndpointMeta(BaseModel):
    host: Optional[str] = Field("localhost", description="Connection host")
    port: Optional[str | int] = Field(8000, description="Connection port")

    @property
    def port_int(self) -> int | None:
        if self.port and isinstance(self.port, str):
            return int(self.port)
        return self.port or None


class AuthMeta(BaseModel):
    username: Optional[str] = Field(None, description="Database username")
    password: Optional[str] = Field(None, description="Database password")


class URIConnectionMeta(BaseModel):
    uri: Optional[str] = Field("", description="Database connection URI")


@deprecated(
    version="0.1.11", reason="use DatabaseConnectionMeta or QueueConnectionMeta instead"
)
class ConnectionMeta(HostMeta):
    """
    Base connection metadata model
    """

    username: Optional[str] = Field(None)
    password: Optional[str] = Field(None)
    database: Optional[Union[str, int]] = Field(None, description="Database name")
    clustersUri: Optional[List[HostMeta]] = Field(None)

    def uri_string(self, base: str = "http", with_db: bool = True) -> str:
        meta = ""
        if self.clustersUri:
            temp = []
            for cluster in self.clustersUri:
                temp.append(f"{cluster.host}:{cluster.port}")
            meta = ",".join(temp)
        else:
            meta = f"{self.host}:{self.port}"
        if self.username:
            return f"{base}://{self.username}:{self.password}@{meta}/{self.database if with_db else ''}"
        return f"{base}://{meta}/{self.database if with_db else ''}"


@deprecated(version="0.2.0", reason="Use DatabaseConnectionMeta instead")
class DatabaseConnectionMeta(HostMeta):

    username: Optional[str] = Field(None)
    password: Optional[str] = Field(None)
    database: Optional[Union[str, int]] = Field(None, description="Database name")
    uri: Optional[str] = Field("", description="")

    def uri_string(self, base: str = "http", with_db: bool = True) -> str:
        meta = f"{self.host}:{self.port}"
        if self.username:
            return f"{base}://{self.username}:{self.password}@{meta}/{self.database if with_db else ''}"
        return f"{base}://{meta}/{self.database if with_db else ''}"

    @model_validator(mode="after")
    def extract_uri(self):
        if self.uri:
            uri = re.sub(r"\w+:(//|/)", "", self.uri)
            metadata, others = (
                re.split(r"\/\?|\/", uri) if re.search(r"\/\?|\/", uri) else [uri, None]
            )
            if others and "&" in others:
                for other in others.split("&"):
                    if "=" in other and re.search(r"authSource", other):
                        self.database = other.split("=")[-1]
                    elif "=" not in other:
                        self.database = other
            if "@" in metadata:
                self.username, self.password, self.host, self.port = re.split(
                    r"\@|\:", metadata
                )
            else:
                self.host, self.port = re.split(r"\:", metadata)
            self.port = int(self.port)
        return self


@deprecated(version="0.2.0", reason="use DBConnectionMeta instead")
class ConnectionUriMeta(ConnectionMeta):
    """Connection with URI and connection types metadata model

    Args:
        ConnectionMeta (BaseModel): Base connection metadata model

    Returns:
        ConnectionMeta: parsed connection metadata from URI
    """

    uri: Optional[str] = Field("", description="")
    type_connection: Optional[connectionType] = Field(
        None, examples=ConnectionTypes.list()
    )

    @model_validator(mode="after")
    def extract_uri(self):
        if self.uri:
            uri = re.sub(r"\w+:(//|/)", "", self.uri)
            metadata, others = (
                re.split(r"\/\?|\/", uri) if re.search(r"\/\?|\/", uri) else [uri, None]
            )
            if others and "&" in others:
                for other in others.split("&"):
                    if "=" in other and re.search(r"authSource", other):
                        self.database = other.split("=")[-1]
                    elif "=" not in other:
                        self.database = other
            if "@" in metadata:
                if "," in metadata:
                    metadata, raw_clusters = re.split(r"\@", metadata)
                    self.username, self.password = re.split(r"\:", metadata)
                    clustersUri = []
                    for cluster in raw_clusters.split(","):
                        hostData = re.split(r"\:", cluster)
                        clustersUri.append(HostMeta(host=hostData[0], port=hostData[1]))
                    self.clustersUri = clustersUri
                else:
                    self.username, self.password, self.host, self.port = re.split(
                        r"\@|\:", metadata
                    )
            else:
                self.host, self.port = re.split(r"\:", metadata)
            self.port = int(self.port)
        return self


class DBConnectionMeta(EndpointMeta, AuthMeta, URIConnectionMeta):
    database: Optional[str] = Field(None, description="Database name")
    space: Optional[str] = Field(None, description="Database schema / space name")
    connection_type: Optional[str] = Field(None, description="Database connection type")

    def uri_string(self, base: str = "http", with_db: bool = True) -> str:
        """
        Return a URI string for the database connection.

        :param base: The base of the URI (e.g. "http", "postgresql", etc.).
        :param with_db: Whether to include the database name in the URI.
        :return: A string representing the URI.
        """
        if self.host:
            meta = f"{self.host}:{self.port}"
            if self.username:
                return f"{base}://{self.username}:{self.password}@{meta}/{self.database if with_db and self.database else ''}"
            return (
                f"{base}://{meta}/{self.database if with_db and self.database else ''}"
            )
        return ""

    @model_validator(mode="after")
    def extract_uri(self):
        """
        Extracts and parses the URI to populate the connection metadata fields.

        This method processes the `uri` attribute to extract authentication and
        connection details such as username, password, host, port, and database.
        It modifies the respective attributes of the instance based on the parsed
        URI components.

        Steps involved:
        - Strips the scheme from the URI.
        - Splits the URI into metadata and additional query parameters.
        - Extracts database name from query parameters if present.
        - Parses authentication info and host details from the metadata.
        - Converts the port to an integer.

        Returns:
            The instance with populated connection metadata fields.
        """
        if self.uri:
            uri = re.sub(r"\w+:(//|/)", "", self.uri)
            metadata, others = (
                re.split(r"\/\?|\/", uri) if re.search(r"\/\?|\/", uri) else [uri, None]
            )
            if others and not self.database:
                if "&" in others:
                    for other in others.split("&"):
                        if "=" in other and re.search(r"authSource", other):
                            self.database = other.split("=")[-1]
                        elif "=" not in other:
                            self.database = other
                else:
                    self.database = others
            if "@" in metadata:
                self.username, self.password, self.host, self.port = re.split(
                    r"\@|\:", metadata
                )
            else:
                self.host, self.port = re.split(r"\:", metadata)
            if self.port:
                self.port = int(self.port)
        return self


class ClusterConnectionMeta(AuthMeta, URIConnectionMeta):
    cluster_uri: Optional[list[EndpointMeta]] = Field(
        [], description="List of clusters endpoint"
    )
    database: Optional[str] = Field(None, description="Database name")
    space: Optional[str] = Field(None, description="Database schema / space name")
    connection_type: Optional[str] = Field(None, description="Database connection type")

    def uri_string(self, base: str = "http", with_db: bool = True) -> str:
        """
        Return a URI string for the database connection.

        :param base: The base of the URI (e.g. "http", "postgresql", etc.).
        :param with_db: Whether to include the database name in the URI.
        :return: A string representing the URI.
        """
        if self.cluster_uri:
            meta = ",".join([f"{c.host}:{c.port}" for c in self.cluster_uri])
            if self.username:
                return f"{base}://{self.username}:{self.password}@{meta}/{self.database if with_db and self.database else ''}"
            return (
                f"{base}://{meta}/{self.database if with_db and self.database else ''}"
            )
        return ""

    @model_validator(mode="after")
    def extract_uri(self):
        """
        Extract URI from connection string and fill in the respective fields.

        If the connection string is in the format of mongodb://user:password@host:port/database,
        the respective fields will be filled in. If the connection string is in the format of
        mongodb://host:port,host:port/database, the hosts will be split into a list of
        EndpointMeta objects.

        :return: The modified ClusterConnectionMeta object.
        :rtype: ClusterConnectionMeta
        """
        if self.uri:
            uri = re.sub(r"\w+:(//|/)", "", self.uri)
            clean_meta, others = (
                re.split(r"\/\?|\/", uri) if re.search(r"\/\?|\/", uri) else [uri, None]
            )
            cluster_uri = []
            if others and not self.database:
                if "&" in others:
                    for other in others.split("&"):
                        if "=" in other and re.search(r"authSource", other):
                            self.database = other.split("=")[-1]
                        elif "=" not in other:
                            self.database = other
                else:
                    self.database = others
            if "@" in clean_meta:
                auth_meta, clean_meta = re.split(r"\@", clean_meta)
                self.username, self.password = re.split(r"\:", auth_meta)

            for cluster in clean_meta.split(","):
                hostData = re.split(r"\:", cluster)
                cluster_uri.append(
                    EndpointMeta(host=hostData[0], port=int(hostData[1]))
                )
            self.cluster_uri = cluster_uri
        return self


class S3ConnectionMeta(EndpointMeta):
    access_key: Optional[str] = Field(None, description="S3 access key")
    secret_key: Optional[str] = Field(None, description="S3 secret key")
    bucket: str = Field(..., description="S3 bucket name")
    base_path: Optional[str] = Field("/", description="S3 base path")

    @property
    def json_meta(self) -> dict:
        """
        Return a dictionary of metadata for connecting to S3.

        :return: A dictionary with the endpoint_url, access_key, and secret_key.
        """
        return {
            "endpoint_url": f"http://{self.host}:{self.port}",
            "key": self.access_key,
            "secret": self.secret_key,
        }


class DatasetMeta(BaseModel):
    connection_meta: Optional[
        DBConnectionMeta | ClusterConnectionMeta | S3ConnectionMeta | str
    ] = Field(None, description="Connection metadata")
    name: str = Field(
        ...,
        description="Name of the dataset, it can refer to a path / to a file / a name of a / table in a database",
    )
    tags: Optional[list[str]] = Field([], description="Tags for the dataset")


class RedisConnectionMeta(EndpointMeta, AuthMeta):
    database: int = Field(..., description="Database name")


class RMQConnectionMeta(EndpointMeta, AuthMeta):
    vhost: Optional[str] = Field(None, description="Virtual host")


class KafkaMeta(BaseModel):
    bootstrap_servers: str | list[str]
    session_timeout: Optional[int] = Field(6000, description="in milliseconds")
    auto_offset_reset: Optional[str] = Field("earliest")

    @model_validator(mode="after")
    def extract_uri(self):
        if isinstance(self.bootstrap_servers, list):
            self.bootstrap_servers = ",".join(self.bootstrap_servers)
        return self

    def confluent_config(self, **kwargs) -> dict:
        return {
            "bootstrap.servers": self.bootstrap_servers,
            "session.timeout.ms": self.session_timeout,
            "auto.offset.reset": self.auto_offset_reset,
            **kwargs,
        }


database_meta_type = TypeVar("database_meta_type", DatabaseConnectionMeta, HostMeta)
queue_meta_type = TypeVar("queue_meta_type", DatabaseConnectionMeta, HostMeta)
connectionPayload = TypeVar("connectionPayload", ConnectionMeta, ConnectionUriMeta)


@deprecated(version="0.1.11", reason="use DatabaseConnector or QueueConnector instead")
class BaseConnection(ABC):
    def __init__(self, metadata: connectionPayload) -> None:
        self._metadata = metadata

    @abstractmethod
    def close(self) -> None:
        pass


class BaseConnector(ABC):
    def __init__(self) -> None:
        pass


@deprecated(
    version="0.1.14",
    reason="Now databaseConnector split into SQLConnector and NoSQLConnector",
)
class DatabaseConnector(BaseConnector):
    def __init__(self, meta: database_meta_type) -> None:
        self._meta: database_meta_type = meta
        pass

    @abstractmethod
    def connect(self, **kwargs):
        pass

    @abstractmethod
    def get(self, table: str, query: Any, **kwargs):
        pass

    @abstractmethod
    def get_all(self, table: str, query: Any, **kwargs):
        pass

    @abstractmethod
    def insert(self, table: str, data: Any, **kwargs):
        pass

    @abstractmethod
    def insert_many(self, table: str, data: List[Any], **kwargs):
        pass

    @abstractmethod
    def update(self, table: str, query: Any, data: Any, **kwargs):
        pass

    @abstractmethod
    def delete(self, table: str, query: Any, **kwargs):
        pass

    @abstractmethod
    def close(self):
        pass


class NosqlConnector(BaseConnector):
    def __init__(self, meta: database_meta_type) -> None:
        self._meta: database_meta_type = meta
        pass

    @abstractmethod
    def connect(self, **kwargs):
        pass

    @abstractmethod
    def get(self, dataset: str, query: Any, **kwargs):
        pass

    @abstractmethod
    def get_all(self, dataset: str, query: Any, **kwargs):
        pass

    @abstractmethod
    def insert(self, dataset: str, data: Any, **kwargs):
        pass

    @abstractmethod
    def insert_many(self, dataset: str, data: List[any], **kwargs):
        pass

    @abstractmethod
    def update(self, dataset: str, query: Any, data: Any, **kwargs):
        pass

    @abstractmethod
    def delete(self, dataset: str, query: Any, **kwargs):
        pass

    @abstractmethod
    def close(self):
        pass


class SQLConnector(BaseConnector):
    def __init__(self, meta: database_meta_type) -> None:
        self._meta: database_meta_type = meta
        pass

    @abstractmethod
    def connect(self, **kwargs):
        pass

    @abstractmethod
    def get(self, query: Any, **kwargs):
        pass

    @abstractmethod
    def get_all(self, query: Any, **kwargs):
        pass

    @abstractmethod
    def close(self):
        pass


class QueueConnector(BaseConnector):
    def __init__(self, meta: queue_meta_type) -> None:
        self._meta: queue_meta_type = meta
        pass

    @abstractmethod
    def consumer_connect(self, queue: str, **kwargs):
        pass

    @abstractmethod
    def producer_connect(self, queue: str, **kwargs):
        pass

    @abstractmethod
    def consumer_close(self):
        pass

    @abstractmethod
    def producer_close(self):
        pass
