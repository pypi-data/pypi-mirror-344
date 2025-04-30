from bunq.sdk.model.generated.endpoint import RequestInquiryApiObject
from bunq.sdk.model.generated.endpoint import RequestResponseApiObject
from bunq.sdk.model.generated.object_ import AmountObject
from tests.bunq_test import BunqSdkTestCase


class TestRequestEnquiry(BunqSdkTestCase):
    """
    Tests:
        RequestInquiryApiObject
        RequestResponseApiObject
    """

    _REQUEST_AMOUNT_EUR = '0.01'
    _REQUEST_CURRENCY = 'EUR'
    _DESCRIPTION = 'Python unit test request'
    _FIELD_STATUS = 'status'
    _STATUS_ACCEPTED = 'ACCEPTED'
    _STATUS_PENDING = 'PENDING'

    def test_sending_and_accepting_request(self):
        """
        Tests sending a request from monetary account 1 to monetary account 2
        and accepting this request

        This test has no assertion as of its testing to see if the code runs
        without errors
        """

        self.send_request()

        url_params_count_only_expected = {
            self._FIELD_STATUS: self._STATUS_PENDING
        }

        request_response_id = RequestResponseApiObject.list(self._second_monetary_account.id_, url_params_count_only_expected).value[self._FIRST_INDEX].id_

        self.accept_request(request_response_id)

    def send_request(self) -> None:
        RequestInquiryApiObject.create(
            AmountObject(self._REQUEST_AMOUNT_EUR, self._REQUEST_CURRENCY),
            self._get_alias_second_account(),
            self._DESCRIPTION,
            False
        )

    def accept_request(self, response_id: int) -> None:
        RequestResponseApiObject.update(
            response_id,
            self._second_monetary_account.id_,
            None,
            self._STATUS_ACCEPTED
        )