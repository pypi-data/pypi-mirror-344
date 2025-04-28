"""This module provides utilities for managing cloud resources.

Attributes:
    CloudType (Enum): The cloud providers supported by the Cloud class.
    gcloud (SysCmdRunner.run): A simple interface to the gcloud command line tool.
"""

# Import standard modules
from ast import literal_eval
from enum import Enum
from os import getenv
from pathlib import Path
from string import Template
from typing import Any, List, Optional, Sequence

# Import third-party modules
from docker import DockerClient
from docker.errors import ImageNotFound
from docker.models.containers import Container as DockerContainer
from requests import head as get_head

# Import internal modules
from .lang import BatCaveError, BatCaveException, CommandResult, WIN32
from .sysutil import SysCmdRunner

CloudType = Enum('CloudType', ('local', 'gcloud', 'dockerhub'))

# pylint: disable=invalid-name
if WIN32:
    user_install = Path(getenv('USERPROFILE', '')) / 'APPDATA/LOCAL'
    gcloud_command_location = 'Google/Cloud SDK/google-cloud-sdk/bin/gcloud.cmd'
    if (user_install / gcloud_command_location).exists():
        gcloud_command = str(user_install / gcloud_command_location)
    else:
        gcloud_command = str(Path(getenv('ProgramFiles(x86)', '')) / gcloud_command_location)
else:
    gcloud_command = 'gcloud'
gcloud = SysCmdRunner(gcloud_command, quiet=True, syscmd_args={'use_shell': WIN32}).run
# pylint: enable=invalid-name


class CloudError(BatCaveException):
    """Cloud Exceptions.

    Attributes:
        IMAGE_ERROR: There was an error working with a container image.
        INVALID_OPERATION: The specified cloud type does not support the requested operation.
        INVALID_TYPE: An invalid cloud type was specified.
    """
    IMAGE_ERROR = BatCaveError(1, Template('Error ${action}ing image: $err'))
    INVALID_OPERATION = BatCaveError(2, Template('Invalid Cloud type ($ctype) for this operation'))
    INVALID_TYPE = BatCaveError(3, Template('Invalid Cloud type ($ctype). Must be one of: ' + str([t.name for t in CloudType])))


class Cloud:
    """Class to create a universal abstract interface for a cloud instance."""

    def __init__(self, ctype: CloudType, /, *, auth: Sequence[str] = ('', ''), login: bool = True):
        """
        Args:
            ctype: The cloud provider for this instance. Must be a member of CloudType.
            auth (optional, default=None): This is a (username, password) tuple.
            login (optional, default=True): Whether or not to login to the cloud provider at instance initialization.

        Attributes:
            auth: The value of the auth argument.
            _client: A reference to the underlying client API object.
            _type: The value of the ctype argument.
        """
        self._client: Any = False
        self._type = ctype
        self.auth = (auth[0], auth[1])
        validate_type(self.type)
        if login:
            self.login()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        return False

    client = property(lambda s: s._client, doc='A read-only property which returns the client reference.')
    type = property(lambda s: s._type, doc='A read-only property which returns the cloud type.')

    def exec(self, *args, **kwargs) -> CommandResult:
        """Execute a command against the cloud API.

        Args:
            *args (optional, default=[]): A list of arguments to pass to the API.
            **kwargs (optional, default={}): A dictionary to pass to the API.

        Returns:
            The result of the API call.

        Raises:
            CloudError.INVALID_OPERATION: If the cloud type does not support an API call.
        """
        match self.type:
            case CloudType.gcloud:
                return gcloud(*args, **kwargs)
        raise CloudError(CloudError.INVALID_OPERATION, ctype=self.type.name)

    def get_container(self, name: str, /) -> 'Container':
        """Get a container from the cloud.

        Args:
            name: The container name to retrieve.

        Returns:
            The container object.
        """
        return Container(self, name)

    def get_containers(self, filters: Optional[str] = None, /) -> List['Container']:
        """Get a possibly filtered list of containers.

        Args:
            filter (optional, default=None): the container name to retrieve.

        Returns:
            The container object.

        Raises:
            CloudError.INVALID_OPERATION: If the cloud type does not support login.
        """
        match self.type:
            case CloudType.local | CloudType.dockerhub:
                return [Container(self, c.name) for c in self._client.containers.list(filters=filters)]
        raise CloudError(CloudError.INVALID_OPERATION, ctype=self.type.name)

    containers = property(get_containers, doc='A read-only property which calls the get_containers() method with no filters.')

    def get_image(self, tag: str, /) -> 'Image':
        """Get an image from the cloud container registry.

        Args:
            tag: The container image tag to retrieve.

        Returns:
            The image object.
        """
        return Image(self, tag)

    def login(self) -> None:
        """Perform a login to the cloud provider.

        Returns:
            Nothing.
        """
        self._client = DockerClient()
        if self.type == CloudType.dockerhub:
            self._client.login(*self.auth)


class Image:
    """Class to create a universal abstract interface to a container image."""

    def __init__(self, cloud: Cloud, name: str, /):
        """
        Args:
            cloud: The API cloud reference.
            name: The image name.

        Attributes:
            _cloud: The value of the cloud argument.
            _docker_client: A reference to the client from the Docker API.
            _name: The value of the name argument.
            _ref: A reference to the underlying API object.
        """
        self._cloud = cloud
        self._name = name
        self._docker_client: DockerClient = self.cloud.client if isinstance(self.cloud.client, DockerClient) else DockerClient()
        if self._cloud.type == CloudType.dockerhub:
            (image, tag) = self.name.split(':', 1)
            response = get_head(f'https://registry.hub.docker.com/v2/{image}/manifests/{tag}', auth=self._cloud.auth,
                                headers={"Accept": "application/vnd.docker.distribution.manifest.v2+json"}, timeout=10)
            if response.status_code != 200:
                self._ref = None
        try:
            self._ref = self.cloud.client.images.get(self.name)
        except ImageNotFound:
            self._ref = None

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        return False

    cloud = property(lambda s: s._cloud, doc='A read-only property which returns the container cloud object.')
    name = property(lambda s: s._name, doc='A read-only property which returns the name of the image.')

    containers = property(lambda s: s.cloud.get_containers({'ancestor': s.name}),
                          doc='A read-only property which returns all the containers for this image.')

    def get_tags(self) -> List[str]:
        """Get a list of tags applied to the image.

        Returns:
            The sorted list of tags applied to the image.
        """
        return self._ref.tags if self._ref else []

    tags = property(get_tags, doc='A read-only property which calls the get_tags() method with no filters.')

    def pull(self) -> 'Image':
        """Pull the image from the registry.

        Returns:
            The image object.
        """
        self._ref = self._docker_client.images.pull(self.name)
        return self

    def push(self) -> List[str]:
        """Push the image to the registry.

        Returns:
            The server log from the push.
        """
        docker_log = [literal_eval(line.strip()) for line in self._docker_client.images.push(self.name).splitlines() if line]
        errors = [line['error'] for line in docker_log if 'error' in line]
        if errors:
            raise CloudError(CloudError.IMAGE_ERROR, action='push', err=''.join(errors))
        return docker_log

    def run(self, *, detach: bool = True, update: bool = True, **kwargs) -> DockerContainer:
        """Run an image to create an active container.

        Args:
            detach (optional, default=True): If True, do not wait for the container to complete.
            update (optional, default=True): If True, perform a pull of the image from the registry before running.
            **kwargs (optional, default={}): A dictionary of arguments to pass to the run command.

        Returns:
            A reference to the active container.

        Raises:
            CloudError.INVALID_OPERATION: If the cloud type does not support running an image.
        """
        if update:
            self.pull()
        match self.cloud.type:
            case CloudType.local | CloudType.dockerhub:
                return self.cloud.client.containers.run(self.name, detach=detach, **kwargs)
        raise CloudError(CloudError.INVALID_OPERATION, ctype=self.cloud.type.name)

    def tag(self, new_tag: str, /) -> Optional['Image']:
        """Tag an image in the registry.

        Returns:
            The tagged image.
        """
        new_ref: Optional[Image] = None
        self.pull()
        if self._ref is None:
            raise CloudError(CloudError.IMAGE_ERROR, action='tag', err='Image not found')
        self._ref.tag(new_tag)
        (new_ref := Image(self.cloud, new_tag)).push()
        return new_ref


class Container:
    """Class to create a universal abstract interface to a container."""

    def __init__(self, cloud: Cloud, name: str, /):
        """
        Args:
            cloud: The API cloud reference.
            name: The container name.

        Attributes:
            _cloud: The value of the cloud argument.
            _name: The value of the name argument.
            _ref: A reference to the underlying API object.

        Raises:
            CloudError.INVALID_OPERATION: If the specified cloud type is not supported.
        """
        self._cloud = cloud
        self._name = name
        self._ref: Any = None
        match self.cloud.type:
            case CloudType.local | CloudType.dockerhub:
                self._ref = self.cloud.client.containers.get(self.name)
            case _:
                raise CloudError(CloudError.INVALID_OPERATION, ctype=self.cloud.type.name)

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        return False

    cloud = property(lambda s: s._cloud, doc='A read-only property which returns the container cloud object.')
    name = property(lambda s: s._name, doc='A read-only property which returns the name of the container.')

    def stop(self) -> DockerContainer:
        """Stop a running container.

        Returns:
            A reference to the stopped container.

        Raises:
            CloudError.INVALID_OPERATION: If the cloud type does not support stopping an container.
        """
        match self.cloud.type:
            case CloudType.local | CloudType.dockerhub:
                return self._ref.stop()
        raise CloudError(CloudError.INVALID_OPERATION, ctype=self.cloud.type.name)


def validate_type(ctype: CloudType) -> None:
    """Determine if the specified Cloud type is valid.

    Args:
        ctype: The Cloud type.

    Returns:
        Nothing.

    Raises
        CloudError.INVALID_TYPE: If the cloud type is not valid.
    """
    if ctype not in CloudType:
        raise CloudError(CloudError.INVALID_TYPE, ctype=ctype)

# cSpell:ignore dockerhub syscmd
