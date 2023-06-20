from enum import Enum


class CommuniqueType(Enum):
    STATUS = 'StatusCommunique'
    TRANSFER_STATUS = 'TransferStatusCommunique'
    # CONFIRMATION = 'ConfirmationCommunique'
    # REJECTION = 'RejectionCommunique'
    BROADCAST = 'BroadcastCommunique'
    TRANSFER = 'TransferCommunique'
    INITIALISE_DOWNLOAD = 'InitialiseDownloadCommunique'
    INITIALISE_TRANSFER = 'InitialiseTransferCommunique'

    @staticmethod
    def types():
        return {
            c.value for c in CommuniqueType
        }
