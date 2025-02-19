import uuid

from yandex_checkout.client import ApiClient
from yandex_checkout.domain.common.http_verb import HttpVerb
from yandex_checkout.domain.request.capture_payment_request import CapturePaymentRequest
from yandex_checkout.domain.request.payment_request import PaymentRequest
from yandex_checkout.domain.response.payment_list_responce import PaymentListResponse
from yandex_checkout.domain.response.payment_response import PaymentResponse


class Payment:
    base_path = '/payments'

    @classmethod
    def find_one(cls, payment_id, client):
        """
        Get information about payment

        :param payment_id:
        :return: PaymentResponse
        """
        instance = cls()
        if not isinstance(payment_id, str) or not payment_id:
            raise ValueError('Invalid payment_id value')

        path = instance.base_path + '/' + payment_id
        response = client.request(HttpVerb.GET, path)
        return PaymentResponse(response)

    @classmethod
    def create(cls, params, client, idempotency_key=None):
        """
        Create payment

        :param params: data passed to API
        :param idempotency_key:
        :return: PaymentResponse
        """
        instance = cls()
        path = cls.base_path

        if not idempotency_key:
            idempotency_key = uuid.uuid4()

        headers = {
            'Idempotence-Key': str(idempotency_key)
        }

        if isinstance(params, dict):
            params_object = PaymentRequest(params)
        elif isinstance(params, PaymentRequest):
            params_object = params
        else:
            raise TypeError('Invalid params value type')

        response = client.request(HttpVerb.POST, path, None, headers, params_object)
        return PaymentResponse(response)

    @classmethod
    def capture(cls, payment_id, client, params=None, idempotency_key=None):
        """
        Capture payment

        :param payment_id:
        :param params: data passed to capture payment
        :param idempotency_key:
        :return: PaymentResponse
        """
        instance = cls()
        if not isinstance(payment_id, str) or not payment_id:
            raise ValueError('Invalid payment_id value')

        path = instance.base_path + '/' + payment_id + '/capture'

        if not idempotency_key:
            idempotency_key = uuid.uuid4()

        headers = {
            'Idempotence-Key': str(idempotency_key)
        }

        if isinstance(params, dict):
            params_object = CapturePaymentRequest(params)
        elif isinstance(params, CapturePaymentRequest):
            params_object = params
        else:
            params_object = None

        response = client.request(HttpVerb.POST, path, None, headers, params_object)
        return PaymentResponse(response)

    @classmethod
    def cancel(cls, payment_id, client, idempotency_key=None):
        """
        Cancel payment

        :param payment_id:
        :param idempotency_key:
        :return: PaymentResponse
        """
        instance = cls()
        if not isinstance(payment_id, str) or not payment_id:
            raise ValueError('Invalid payment_id value')

        if not idempotency_key:
            idempotency_key = uuid.uuid4()

        path = instance.base_path + '/' + payment_id + '/cancel'
        headers = {
            'Idempotence-Key': str(idempotency_key)
        }
        response = client.request(HttpVerb.POST, path, None, headers)
        return PaymentResponse(response)

    @classmethod
    def list(cls, client, params):
        instance = cls()
        path = cls.base_path

        response = client.request(HttpVerb.GET, path, params)
        return PaymentListResponse(response)
