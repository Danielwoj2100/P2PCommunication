from communiques.Communique import Communique
from communiques.enums.StatusCode import StatusCode


class StatusCommunique(Communique):
    status_code: StatusCode

    def __init__(
        self, *,
        senders_address=None,
        port=None,
        communique_type=None,
        checksum=None,
        status_code=None
    ):
        super().__init__(
            senders_address=senders_address,
            port=port,
            communique_type=communique_type,
            checksum=checksum
        )
        self.status_code = status_code

    def __str__(self):
        starting_representation = super().__str__()
        addon = self.status_code.value
        return starting_representation + addon + '|'

