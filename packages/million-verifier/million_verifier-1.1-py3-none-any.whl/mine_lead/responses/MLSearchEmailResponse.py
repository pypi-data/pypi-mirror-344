from src.mine_lead.responses import MLResponse


class MLSearchEmailResponse(MLResponse):
    email: str = None
    verified: bool = False
    saved: bool = False

    def __init__(self, data):
        super().__init__(data)