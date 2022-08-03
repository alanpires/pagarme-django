from rest_framework.exceptions import APIException

class ExpiredCardError(APIException):
    status_code = 400
    default_detail = {
	            "error": [
		            "Expired card, try to register another valid card"
	            ]
            }

class CreatePaymentInfoError(APIException):
    status_code = 422
    default_detail = {
	            "error": [
		            "This card is already registered for this user"
	            ]
            }

class ProductsFromDifferentSellersAndDoesNotExistAndNotAvailableAndIsNotActiveError(APIException):
    status_code = 400
    default_detail = {
	            "error": [
		            "All products must belong to the same seller",  "Product does not exist", "Product is not available", "Product is not active"
	            ]
            }

class ExpiredCardError(APIException):
    status_code = 400
    default_detail = {
	            "error": [
		            "This card is expired"
	            ]
            }

class PaymentInfoMissingException(APIException):
    status_code = 400
    default_detail = {
	"payment_info": [
		"This field is required."
	]
}