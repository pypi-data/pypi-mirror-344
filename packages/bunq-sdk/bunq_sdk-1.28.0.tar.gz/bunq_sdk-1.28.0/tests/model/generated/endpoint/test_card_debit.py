import random
import string

from bunq.sdk.context.bunq_context import BunqContext
from bunq.sdk.model.generated.endpoint import CardApiObject
from bunq.sdk.model.generated.endpoint import CardDebitApiObject
from bunq.sdk.model.generated.endpoint import CardNameApiObject
from bunq.sdk.model.generated.object_ import CardPinAssignmentObject
from tests.bunq_test import BunqSdkTestCase


class TestCardDebit(BunqSdkTestCase):
    """
    Tests:
        CardApiObject
        CardDebitApiObject
        CardNameApiObject
    """

    _CARD_PIN_CODE = '4045'
    _SECOND_LINE_LENGTH_MAXIMUM = 20
    _STRING_EMPTY = ''
    _PIN_CODE_ASSIGNMENT_TYPE_PRIMARY = 'PRIMARY'
    _CARD_TYPE_MASTERCARD = 'MASTERCARD'
    _PRODUCT_TYPE_MASTERCARD_DEBIT = 'MASTERCARD_DEBIT'
    _CARD_ROUTING_TYPE = 'MANUAL'

    def test_order_debit_card(self):
        """
        Tests ordering a new card and checks if the fields we have entered
        are indeed correct by retrieving the card from the card endpoint and
        checks this date against the data we have submitted
        """

        second_line = self.second_line_random
        pin_code_assignment = CardPinAssignmentObject(
            self._PIN_CODE_ASSIGNMENT_TYPE_PRIMARY,
            self._CARD_ROUTING_TYPE,
            self._CARD_PIN_CODE,
            BunqContext.user_context().primary_monetary_account.id_
        )

        card_debit = CardDebitApiObject.create(
            second_line=second_line,
            name_on_card=self.card_name_allowed,
            type_=self._CARD_TYPE_MASTERCARD,
            product_type=self._PRODUCT_TYPE_MASTERCARD_DEBIT,
            alias=self.alias_first,
            pin_code_assignment=[pin_code_assignment]
        ).value

        card = CardApiObject.get(card_debit.id_).value

        self.assertEqual(self.card_name_allowed, card.name_on_card)
        self.assertEqual(second_line, card.second_line)
        self.assertEqual(card_debit.created, card.created)

    @property
    def card_name_allowed(self) -> str:
        return CardNameApiObject.list().value[self._FIRST_INDEX].possible_card_name_array[self._FIRST_INDEX]

    @property
    def second_line_random(self) -> str:
        second_line_characters = []

        for _ in range(self._SECOND_LINE_LENGTH_MAXIMUM):
            next_char = random.choice(string.ascii_uppercase)
            second_line_characters.append(next_char)

        return self._STRING_EMPTY.join(second_line_characters)
