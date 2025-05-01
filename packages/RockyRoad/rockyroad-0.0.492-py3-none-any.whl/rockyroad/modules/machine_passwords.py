from .module_imports import key
from uplink.retry.when import status_5xx
from uplink import (
    Consumer,
    get as http_get,
    post,
    patch,
    delete,
    returns,
    headers,
    retry,
    Body,
    json,
    Query,
)


@headers({"Ocp-Apim-Subscription-Key": key})
@retry(max_attempts=20, when=status_5xx())
class Machine_Passwords(Consumer):
    """Inteface to machine logs resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._base_url
        super().__init__(base_url=Resource._base_url, *args, **kw)

    def requests(self):
        """Inteface to Machine Password Requests resource for the RockyRoad API."""
        return self._Requests(self)

    @returns.json
    @http_get("machines-passwords/generate")
    def generate(self, machine_uid: Query = None, model: Query = None, serial: Query = None):
        """This call will generate a new password for the specified machine."""

    @returns.json
    @http_get("machines-passwords/verify")
    def verify(self, machine_uid: Query = None, model: Query = None, serial: Query = None):
        """This call will verify the password for the specified machine."""

    @headers({"Ocp-Apim-Subscription-Key": key})
    @retry(max_attempts=20, when=status_5xx())
    class _Requests(Consumer):
        """Inteface to Machine Password Requests resource for the RockyRoad API."""

        def __init__(self, Resource, *args, **kw):
            self._base_url = Resource._base_url
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @http_get("machines-passwords/requests")
        def list(self):
            """This call will return a list of machine password requests."""

        @returns.json
        @json
        @post("machines-passwords/requests")
        def insert(self, machine_password_request: Body):
            """This call will create a machine password request with the specified parameters."""

        @returns.json
        @delete("machines-passwords/requests/{uid}")
        def delete(self, uid: Query):
            """This call will delete the machine password request for the specified uid."""
