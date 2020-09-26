from app import BASE_URL


class ApproveApi:
    def __init__(self):
        self.approve_url = BASE_URL + "/member/realname/approverealname"

    def approve(self, session, realname, card_id):
        approve_data = {"realname": realname, "card_id": card_id}
        return session.post(self.approve_url, data=approve_data, files={"x": "y"})
