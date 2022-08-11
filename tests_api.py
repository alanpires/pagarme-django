from rest_framework.test import APIClient, APITestCase
from payment_info.models import PaymentInfo
from payables.models import Payable

class TestAccounst(APITestCase):
    @classmethod
    def setUpTestData(cls):

        cls.admin_data = {
            'email': "admin@mail.com",
            'password': "admin1234",
            'first_name': "Jane",
            'last_name': "Doe",
            'is_seller': False,
            'is_admin': True
        }

        cls.seller_data = {
            'email': "seller@mail.com",
            'password': "seller1234",
            'first_name': "John",
            'last_name': "Doe",
            'is_seller': True,
            'is_admin': False
        }

        cls.buyer_data = {
            'email': "buyer@mail.com",
            'password': "buyer1234",
            'first_name': "Mary",
            'last_name': "Jane",
            'is_seller': False,
            'is_admin': False
        }

        cls.user_data_wrong = {
            'e-mail': "user@mail.com",
            'password': "user1234",
            'first_name': "Peter",
            'last_name': "Parker",
            'is_admin': False
        }

        cls.admin_login_data = {
            'email': "admin@mail.com",
            'password': "admin1234"   
        }

        cls.seller_login_data = {
            'email': "seller@mail.com",
            'password': "seller1234"
        }

        cls.buyer_login_data = {
            'email': "buyer@mail.com",
            'password': "buyer1234"
        }

        cls.wrong_login_email = {
            'email': "wrong@mail.com",
            'password': "admin1234"   
        }

        cls.wrong_login_password = {
            'email': "admin@mail.com",
            'password': "wrong1234"   
        }

        cls.wrong_login_missing_password_field = {
            'email': "admin@mail.com",
        }

    def test_create_account_admin_success_201(self):
        response = self.client.post(
            "/api/accounts/", self.admin_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", output)
        self.assertIn("email", output)
        self.assertIn("first_name", output)
        self.assertIn("last_name", output)
        self.assertIn("is_seller", output)
        self.assertIn("is_admin", output)

        self.assertNotIn("password", output)

        self.assertEqual(output["email"], self.admin_data["email"])
        self.assertEqual(output["is_admin"], self.admin_data["is_admin"])
        self.assertEqual(output["is_seller"], self.admin_data["is_seller"])


    def test_create_account_seller_success_201(self):
        response = self.client.post(
            "/api/accounts/", self.seller_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", output)
        self.assertIn("email", output)
        self.assertIn("first_name", output)
        self.assertIn("last_name", output)
        self.assertIn("is_seller", output)
        self.assertIn("is_admin", output)

        self.assertNotIn("password", output)

        self.assertEqual(output["email"], self.seller_data["email"])
        self.assertEqual(output["is_admin"], self.seller_data["is_admin"])
        self.assertEqual(output["is_seller"], self.seller_data["is_seller"])


    def test_create_account_buyer_success_201(self):
        response = self.client.post(
            "/api/accounts/", self.buyer_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", output)
        self.assertIn("email", output)
        self.assertIn("first_name", output)
        self.assertIn("last_name", output)
        self.assertIn("is_seller", output)
        self.assertIn("is_admin", output)

        self.assertNotIn("password", output)

        self.assertEqual(output["email"], self.buyer_data["email"])
        self.assertEqual(output["is_admin"], self.buyer_data["is_admin"])
        self.assertEqual(output["is_seller"], self.buyer_data["is_seller"])


    def test_create_account_duplicated_email_fail_400(self):
        # Trying to create the same user twice
        self.client.post("/api/accounts/", self.buyer_data, format="json")
        response = self.client.post(
            "/api/accounts/", self.buyer_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertNotIn("id", output)
        

    def test_create_account_wrong_fields_fail_400(self):
        # Trying to create user with wrong fields
        response = self.client.post(
            "/api/accounts/", self.user_data_wrong, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertNotIn("id", output)
        self.assertIn("email", output)
        self.assertIn("is_seller", output)


    def test_login_success_200(self):
        # Creating admin user for testing login
        self.client.post("/api/accounts/", self.admin_data, format="json")

        response = self.client.post(
            "/api/login/", self.admin_login_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", output)


    def test_login_fail_401(self):
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # Trying to login with wrong email
        response = self.client.post(
            "/api/login/", self.wrong_login_email, format="json")

        self.assertEqual(response.status_code, 401)

        # Trying to login with wrong password
        response = self.client.post(
            "/api/login/", self.wrong_login_password, format="json")

        self.assertEqual(response.status_code, 401)


    def test_login_failure_wrong_fields_400(self):
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # Trying to login without password field
        response = self.client.post(
            "/api/login/", 
            self.wrong_login_missing_password_field, 
            format="json")
            
        output = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("password", output)
    

    def test_admin_list_users_success_200(self):
        # Creating and login with admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.get("/api/accounts/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(output, list)
        self.assertEqual(len(output), 1)


    def test_seller_list_users_fail_403(self):
        # Creating and login with seller user
        self.client.post("/api/accounts/", self.seller_data, format="json")
        token = self.client.post(
            "/api/login/", self.seller_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.get("/api/accounts/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            output,
            {'detail': 'You do not have permission to perform this action.'})


    def test_buyer_list_users_fail_403(self):
        # Creating and login with buyer user
        self.client.post("/api/accounts/", self.buyer_data, format="json")
        token = self.client.post(
            "/api/login/", self.buyer_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.get("/api/accounts/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            output,
            {'detail': 'You do not have permission to perform this action.'})


    def test_anonymous_list_users_fail_401(self):
        # Trying to list user without authentication
        response = self.client.get("/api/accounts/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            output,
            {'detail': 'Authentication credentials were not provided.'})
  

class TestFee(APITestCase):

    @classmethod
    def setUpTestData(cls):

        cls.client = APIClient()

        cls.admin_data = {
            'email': "admin@mail.com",
            'password': "admin1234",
            'first_name': "Jane",
            'last_name': "Doe",
            'is_seller': False,
            'is_admin': True
        }
        # Creating admin user
        cls.client.post("/api/accounts/", cls.admin_data, format="json")

        cls.seller_data = {
            'email': "seller@mail.com",
            'password': "seller1234",
            'first_name': "John",
            'last_name': "Doe",
            'is_seller': True,
            'is_admin': False
        }
        
        # Creating seller user
        cls.client.post("/api/accounts/", cls.seller_data, format="json")

        cls.buyer_data = {
            'email': "buyer@mail.com",
            'password': "buyer1234",
            'first_name': "Mary",
            'last_name': "Jane",
            'is_seller': False,
            'is_admin': False
        }
        
        # Creating buyer user
        cls.client.post("/api/accounts/", cls.buyer_data, format="json")


        cls.admin_login_data = {
            'email': "admin@mail.com",
            'password': "admin1234"   
        }

        cls.seller_login_data = {
            'email': "seller@mail.com",
            'password': "seller1234"
        }

        cls.buyer_login_data = {
            'email': "buyer@mail.com",
            'password': "buyer1234"
        }


        cls.fee_data = {
            "credit_fee": "0.06",
            "debit_fee": "0.04",
        }

        cls.fee_data_wrong_fields = {
            "credit": "0.06",
            "debit": "0.04",
        }


    def test_admin_create_fee_success_201(self):
        # Login with admin user
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.post("/api/fee/", self.fee_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", output)
        self.assertIn("credit_fee", output)
        self.assertIn("debit_fee", output)
        self.assertIn("created_at", output)

        self.assertEqual(output["credit_fee"], self.fee_data["credit_fee"])
        self.assertEqual(output["debit_fee"], self.fee_data["debit_fee"])


    def test_admin_create_fee_with_wrong_fields_fail_400(self):
        # Login with admin user
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.post("/api/fee/", self.fee_data_wrong_fields, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertNotIn("id", output)
        self.assertNotIn("created_at", output)
        self.assertIn("credit_fee", output)
        self.assertIn("debit_fee", output)
        

    def test_seller_create_fee_fail_403(self):
        # Login with seller user
        token = self.client.post(
            "/api/login/", self.seller_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.post("/api/fee/", self.fee_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(output, 
            {'detail': 'You do not have permission to perform this action.'})


    def test_buyer_create_fee_fail_403(self):
        # Login with buyer user
        token = self.client.post(
            "/api/login/", self.buyer_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.post("/api/fee/", self.fee_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(output, 
            {'detail': 'You do not have permission to perform this action.'})


    def test_anonymous_create_fee_fail_401(self):
        # Trying to create fee without authentication
        response = self.client.post("/api/fee/", self.fee_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(output, 
            {'detail': 'Authentication credentials were not provided.'})


    def test_admin_list_fee_success_200(self):
        # Login with admin user
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.get("/api/fee/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(output, list)
        self.assertEqual(len(output), 1)


    def test_seller_list_fee_fail_403(self):
        # Login with seller user
        token = self.client.post(
            "/api/login/", self.seller_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.get("/api/fee/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(output, 
            {'detail': 'You do not have permission to perform this action.'})


    def test_buyer_list_fee_fail_403(self):
        # Login with buyer user
        token = self.client.post(
            "/api/login/", self.buyer_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.get("/api/fee/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(output, 
            {'detail': 'You do not have permission to perform this action.'})


    def test_anonymous_list_fee_fail_401(self):
        # Trying to list fees without authentication
        response = self.client.get("/api/fee/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(output, 
            {'detail': 'Authentication credentials were not provided.'})


    def test_admin_retrieve_fee_success_200(self):
        # Login with admin user
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Creating fee and getting fee_id
        fee_id = self.client.post(
            "/api/fee/", self.fee_data, format="json"
        ).json()["id"]

        response = self.client.get(f"/api/fee/{fee_id}/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(output, dict)
        self.assertIn("id", output)
        self.assertIn("created_at", output)
        self.assertEqual(output["id"], fee_id)


    def test_seller_retrieve_fee_fail_403(self):
        # Login with admin user for creating fee
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Creating fee and getting fee_id
        fee_id = self.client.post(
            "/api/fee/", self.fee_data, format="json"
        ).json()["id"]

        # Login with seller user and trying to retrieve fee
        token = self.client.post(
            "/api/login/", self.seller_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.get(f"/api/fee/{fee_id}/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(output, 
            {'detail': 'You do not have permission to perform this action.'})


    def test_buyer_retrieve_fee_fail_403(self):
        # Login with admin user for creating fee
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Creating fee and getting fee_id
        fee_id = self.client.post(
            "/api/fee/", self.fee_data, format="json"
        ).json()["id"]

        # Login with buyer user and trying to retrieve fee
        token = self.client.post(
            "/api/login/", self.buyer_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.get(f"/api/fee/{fee_id}/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(output, 
            {'detail': 'You do not have permission to perform this action.'})


    def test_anonymous_retrieve_fee_fail_401(self):
        # Login with admin user for creating fee
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Creating fee and getting fee_id
        fee_id = self.client.post(
            "/api/fee/", self.fee_data, format="json"
        ).json()["id"]

        # Trying to retrieve fee without authentication
        self.client.credentials()

        response = self.client.get(f"/api/fee/{fee_id}/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(output, 
            {'detail': 'Authentication credentials were not provided.'})



class TestProducts(APITestCase):

    @classmethod
    def setUpTestData(cls):

        cls.client = APIClient()

        cls.admin_data = {
            'email': "admin@mail.com",
            'password': "admin1234",
            'first_name': "Jane",
            'last_name': "Doe",
            'is_seller': False,
            'is_admin': True
        }
        # Creating admin user
        cls.client.post("/api/accounts/", cls.admin_data, format="json")

        cls.seller_data = {
            'email': "seller@mail.com",
            'password': "seller1234",
            'first_name': "John",
            'last_name': "Doe",
            'is_seller': True,
            'is_admin': False
        }
        # Creating seller user
        cls.client.post("/api/accounts/", cls.seller_data, format="json")

        cls.buyer_data = {
            'email': "buyer@mail.com",
            'password': "buyer1234",
            'first_name': "Mary",
            'last_name': "Jane",
            'is_seller': False,
            'is_admin': False
        }
        # Creating buyer user
        cls.client.post("/api/accounts/", cls.buyer_data, format="json")


        cls.admin_login_data = {
            'email': "admin@mail.com",
            'password': "admin1234"   
        }

        cls.seller_login_data = {
            'email': "seller@mail.com",
            'password': "seller1234"
        }

        cls.buyer_login_data = {
            'email': "buyer@mail.com",
            'password': "buyer1234"
        }


        cls.product_data = {
            "description": "Smartband XYZ 3.0",
            "price": 100.99,
            "quantity": 15
        }

        cls.wrong_product_data = {
            "description": "Smartband XYZ 3.0",
            "price": 100.99
        }

        cls.update_product_data = {
            "description": "Smartband XYZ 3.0",
            "price": 99.99,
            "quantity": 20
        }

    
    def test_seller_create_product_success_201(self):
        # Login with seller user for creating product
        token = self.client.post(
            "/api/login/", self.seller_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        response = self.client.post(
            "/api/products/", self.product_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", output)
        self.assertIn("seller", output)
        self.assertIn("description", output)
        self.assertIn("price", output)
        self.assertIn("quantity", output)
        self.assertIn("is_active", output)

        self.assertEqual(output["seller"]["email"], self.seller_data["email"])
        self.assertTrue(output["is_active"])


    def test_seller_create_product_with_wrong_fields_fail_400(self):
        # Login with seller user for creating product
        token = self.client.post(
            "/api/login/", self.seller_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.post(
            "/api/products/", self.wrong_product_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("quantity", output)


    def test_admin_create_product_fail_403(self):
        # Login with admin user for creating product
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.post(
            "/api/products/", self.product_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(output, 
            {'detail': 'You do not have permission to perform this action.'})


    def test_buyer_create_product_fail_403(self):
        # Login with buyer user for creating product
        token = self.client.post(
            "/api/login/", self.buyer_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.post(
            "/api/products/", self.product_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(output, 
            {'detail': 'You do not have permission to perform this action.'})


    def test_anonymous_create_product_fail_401(self):
        # Trying to create product without authentication
        response = self.client.post(
            "/api/products/", self.product_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(output, 
            {'detail': 'Authentication credentials were not provided.'})

    
    def test_list_products_200(self):
        # Listing all products without authentication
        response = self.client.get("/api/products/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(output, list)
        self.assertEqual(output, [])

        # Login with seller user for creating product
        token = self.client.post(
            "/api/login/", self.seller_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        self.client.post("/api/products/", self.product_data, format="json")

        # Cleaning the authentication and trying to list again
        self.client.credentials()
        
        response = self.client.get("/api/products/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(output, list)
        self.assertIsNot(output, [])
        self.assertEqual(len(output), 1)


    def test_retrieve_products_success_200(self):
        # Login with seller user for creating product and getting product_id
        token = self.client.post(
            "/api/login/", self.seller_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        product_id = self.client.post(
            "/api/products/", self.product_data, format="json").json()["id"]

        # Cleaning the authentication and trying to retrieve product
        self.client.credentials()

        response = self.client.get(f"/api/products/{product_id}/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(output, dict)
        self.assertEqual(output["id"], product_id)


    def test_retrieve_products_fail_wrong_id_404(self):
        product_id = "e7177066-a60e-11ec-b909-0242ac120002"

        response = self.client.get(f"/api/products/{product_id}/", format="json")

        self.assertEqual(response.status_code, 404)


    def test_list_products_by_seller_200(self):
        # Login with admin user for getting all users
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Getting seller_id from all users
        users = self.client.get("/api/accounts/", format="json").json()
        seller_id_list = [user["id"] for user in users if user["is_seller"]]
        seller_id = ''.join(seller_id_list)

        # Trying to list products by seller with seller_id
        response = self.client.get(
            f"/api/products/seller/{seller_id}/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(output, list)
        self.assertEqual(output, [])

        # Login with seller user for creating product
        token = self.client.post(
            "/api/login/", self.seller_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        self.client.post("/api/products/", self.product_data, format="json")

        # Cleaning the authentication
        self.client.credentials()

        # Trying to list products by seller again
        response = self.client.get(
            f"/api/products/seller/{seller_id}/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(output, list)
        self.assertIsNot(output, [])
        self.assertEqual(len(output), 1)


    def test_list_products_by_seller_with_wrong_seller_id_404(self):
        # Trying to list products by seller with wrong seller_id
        seller_id = "6e59272a-a611-11ec-b909-0242ac120002"

        response = self.client.get(
            f"/api/products/seller/{seller_id}/", format="json")

        self.assertEqual(response.status_code, 404)
        self.assertDictEqual(response.json(), {"detail": "Not found."})


    def test_seller_update_product_success_200(self):
        # Login with seller user
        token = self.client.post(
            "/api/login/", self.seller_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Creating product and getting product_id
        product_id = self.client.post(
            "/api/products/", self.product_data, format="json"
            ).json()["id"]

        # Trying to update product
        response = self.client.patch(
            f"/api/products/{product_id}/", 
            self.update_product_data, 
            format="json")
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("id", output)
        self.assertIn("description", output)
        self.assertIn("price", output)
        self.assertIn("quantity", output)
        self.assertIn("is_active", output)
        self.assertIn("seller", output)

        self.assertEqual(output["id"], product_id)
        self.assertEqual(output["description"], 
            self.update_product_data["description"])
        self.assertEqual(output["price"], 
            self.update_product_data["price"])
        self.assertEqual(output["quantity"], 
            self.update_product_data["quantity"])
        self.assertTrue(output["is_active"])


    def test_seller_update_product_with_wrong_product_id_404(self):
        # Login with seller user
        token = self.client.post(
            "/api/login/", self.seller_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Invalid product_id
        product_id = "f68425f2-a623-11ec-b909-0242ac120002"

        # Trying to update product
        response = self.client.patch(
            f"/api/products/{product_id}/", 
            self.update_product_data, 
            format="json")

        self.assertEqual(response.status_code, 404)
        

    def test_admin_update_product_fail_403(self):
        # Login with seller user for creating product
        token = self.client.post(
            "/api/login/", self.seller_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Creating product and getting product_id
        product_id = self.client.post(
            "/api/products/", self.product_data, format="json"
            ).json()["id"]

        # Login with admin user
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Trying to update product
        response = self.client.patch(
            f"/api/products/{product_id}/", 
            self.update_product_data, 
            format="json")
        output = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(output, 
            {'detail': 'You do not have permission to perform this action.'})


    def test_buyer_update_product_fail_403(self):
        # Login with seller user for creating product
        token = self.client.post(
            "/api/login/", self.seller_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Creating product and getting product_id
        product_id = self.client.post(
            "/api/products/", self.product_data, format="json"
            ).json()["id"]

        # Login with buyer user
        token = self.client.post(
            "/api/login/", self.buyer_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Trying to update product
        response = self.client.patch(
            f"/api/products/{product_id}/", 
            self.update_product_data, 
            format="json")
        output = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(output, 
            {'detail': 'You do not have permission to perform this action.'})

    def test_anonymous_update_product_fail_401(self):
        # Login with seller user for creating product
        token = self.client.post(
            "/api/login/", self.seller_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Creating product and getting product_id
        product_id = self.client.post(
            "/api/products/", self.product_data, format="json"
            ).json()["id"]

        # Cleaning credentials
        self.client.credentials()

        # Trying to update product
        response = self.client.patch(
            f"/api/products/{product_id}/", 
            self.update_product_data, 
            format="json")
        output = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(output, 
            {'detail': 'Authentication credentials were not provided.'})


class TestPaymentInfo(APITestCase):

    @classmethod
    def setUpTestData(cls):

        cls.client = APIClient()

        cls.admin_data = {
            'email': "admin@mail.com",
            'password': "admin1234",
            'first_name': "Jane",
            'last_name': "Doe",
            'is_seller': False,
            'is_admin': True
        }
        # Creating admin user
        cls.client.post("/api/accounts/", cls.admin_data, format="json")

        cls.seller_data = {
            'email': "seller@mail.com",
            'password': "seller1234",
            'first_name': "John",
            'last_name': "Doe",
            'is_seller': True,
            'is_admin': False
        }
        # Creating seller user
        cls.client.post("/api/accounts/", cls.seller_data, format="json")

        cls.buyer_data = {
            'email': "buyer@mail.com",
            'password': "buyer1234",
            'first_name': "Mary",
            'last_name': "Jane",
            'is_seller': False,
            'is_admin': False
        }
        # Creating buyer user
        cls.client.post("/api/accounts/", cls.buyer_data, format="json")


        cls.admin_login_data = {
            'email': "admin@mail.com",
            'password': "admin1234"   
        }

        cls.seller_login_data = {
            'email': "seller@mail.com",
            'password': "seller1234"
        }

        cls.buyer_login_data = {
            'email': "buyer@mail.com",
            'password': "buyer1234"
        }


        cls.payment_data = {
            "payment_method": "debit",
            "card_number": "1234567812345678",
            "cardholders_name": "MARIANA F SOUZA",
            "card_expiring_date": "2022-04-01",
            "cvv": 456
        }

        cls.wrong_payment_data = {
            "method": "debit",
            "card_number": "1234567812345678",
            "cardholders_name": "MARIANA F SOUZA",
            "card_expiring_date": "2022-04-01",
        }


    def test_buyer_create_payment_info_success_200(self):
        # Login with buyer user 
        token = self.client.post(
            "/api/login/", self.buyer_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.post(
            "/api/payment_info/", self.payment_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", output)
        self.assertIn("payment_method", output)
        self.assertIn("card_number_info", output)
        self.assertIn("cardholders_name", output)
        self.assertIn("card_expiring_date", output)
        self.assertIn("is_active", output)
        self.assertIn("customer", output)
        self.assertNotIn("cvv", output)
        self.assertNotEqual(output["card_number_info"], 
            self.payment_data["card_number"])

    
    def test_buyer_create_payment_info_already_exists_fail_422(self):
        # Login with buyer user 
        token = self.client.post(
            "/api/login/", self.buyer_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Trying to create same card twice
        self.client.post(
            "/api/payment_info/", self.payment_data, format="json")

        response = self.client.post(
            "/api/payment_info/", self.payment_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 422)
        self.assertDictEqual(output, {"error": ["This card is already registered for this user"]})


    def test_buyer_create_payment_info_with_wrong_fields_fail_400(self):
        # Login with buyer user 
        token = self.client.post(
            "/api/login/", self.buyer_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.post(
            "/api/payment_info/", self.wrong_payment_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("payment_method", output)
        self.assertIn("cvv", output)


    def test_seller_create_payment_info_fail_403(self):
        # Login with seller user 
        token = self.client.post(
            "/api/login/", self.seller_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.post(
            "/api/payment_info/", self.payment_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(output, 
            {'detail': 'You do not have permission to perform this action.'})


    def test_admin_create_payment_info_fail_403(self):
        # Login with admin user 
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.post(
            "/api/payment_info/", self.payment_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(output, 
            {'detail': 'You do not have permission to perform this action.'})


    def test_anonymous_create_payment_info_fail_401(self):
        # Trying to create payment info without authentication
        response = self.client.post(
            "/api/payment_info/", self.payment_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(output, 
            {'detail': 'Authentication credentials were not provided.'})



    def test_buyer_list_payment_info_success_200(self):
        # Login with buyer user 
        token = self.client.post(
            "/api/login/", self.buyer_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.get("/api/payment_info/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(output, list)
        self.assertEqual(output, [])

        # Creating a payment info for testing the list again
        self.client.post(
            "/api/payment_info/", self.payment_data, format="json")

        response = self.client.get("/api/payment_info/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(output, list)
        self.assertEqual(len(output), 1)


    def test_seller_list_payment_info_fail_403(self):
        # Login with seller user 
        token = self.client.post(
            "/api/login/", self.seller_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.get("/api/payment_info/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(output, 
            {'detail': 'You do not have permission to perform this action.'})


    def test_admin_list_payment_info_fail_403(self):
        # Login with admin user 
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.get("/api/payment_info/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(output, 
            {'detail': 'You do not have permission to perform this action.'})


    def test_anonymous_list_payment_info_fail_401(self):
        # Trying to list payment info without authentication
        response = self.client.get("/api/payment_info/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(output, 
            {'detail': 'Authentication credentials were not provided.'})


class TestTransactionsAndPayables(APITestCase):
    # extras
    @classmethod
    def setUpTestData(cls):

        cls.client = APIClient()

        # Creating admin user
        cls.admin_data = {
            'email': "admin@mail.com",
            'password': "admin1234",
            'first_name': "Jane",
            'last_name': "Doe",
            'is_seller': False,
            'is_admin': True
        }
        cls.client.post("/api/accounts/", cls.admin_data, format="json")

        cls.admin_login_data = {
            'email': "admin@mail.com",
            'password': "admin1234"   
        }


        # Creating seller user
        cls.seller_data = {
            'email': "seller@mail.com",
            'password': "seller1234",
            'first_name': "John",
            'last_name': "Doe",
            'is_seller': True,
            'is_admin': False
        }
        
        cls.seller_id = cls.client.post(
            "/api/accounts/", cls.seller_data, format="json"
            ).json()["id"]

        # Login with seller for creating 3 products
        cls.seller_login_data = {
            'email': "seller@mail.com",
            'password': "seller1234"
        }

        token = cls.client.post(
            "/api/login/", cls.seller_login_data, format="json"
            ).json()["token"]
        cls.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        cls.products_to_create = [
            {
                "description": "Smartband XYZ 3.0",
                "price": 100.99,
                "quantity": 15,
            },
            {
                "description": "Smartband ABCF 3.0",
                "price": 330.99,
                "quantity": 10,
            },
            {
                "description": "Smartband XPTO 3.0",
                "price": 899.99,
                "quantity": 19,
            }
        ]
        
        # create products seller
        cls.product_id_list = [
            cls.client.post(
                "/api/products/", product, format="json"
                ).json()["id"] 
            for product in cls.products_to_create]

        # Creating seller 2 user
        cls.seller_data_2 = {
            'email': "seller2@mail.com",
            'password': "seller1234",
            'first_name': "John",
            'last_name': "Doe",
            'is_seller': True,
            'is_admin': False
        }
        
        cls.seller_id_2 = cls.client.post(
            "/api/accounts/", cls.seller_data_2, format="json"
            ).json()["id"]

        # Login with seller for creating 3 products
        cls.seller_login_data_2 = {
            'email': "seller2@mail.com",
            'password': "seller1234"
        }

        token = cls.client.post(
            "/api/login/", cls.seller_login_data_2, format="json"
            ).json()["token"]
        cls.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        
        # create products seller
        cls.product_id_list_2 = [
            cls.client.post(
                "/api/products/", product, format="json"
                ).json()["id"] 
            for product in cls.products_to_create]

        # Creating buyer user
        cls.buyer_data = {
            'email': "buyer@mail.com",
            'password': "buyer1234",
            'first_name': "Mary",
            'last_name': "Jane",
            'is_seller': False,
            'is_admin': False
        }
        cls.client.post("/api/accounts/", cls.buyer_data, format="json")

        # Login with buyer user for creating payment info
        cls.buyer_login_data = {
            'email': "buyer@mail.com",
            'password': "buyer1234"
        }

        token = cls.client.post(
            "/api/login/", cls.buyer_login_data, format="json"
            ).json()["token"]
        cls.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        cls.payment_data = {
            "payment_method": "debit",
            "card_number": "1234567812345678",
            "cardholders_name": "MARIANA F SOUZA",
            "card_expiring_date": "2028-04-01",
            "cvv": 456
        }
        
        cls.payment_data_2 = {
            "payment_method": "credit",
            "card_number": "1234567812345678",
            "cardholders_name": "MARIANA F SOUZA",
            "card_expiring_date": "2030-04-01",
            "cvv": 123
        }

        cls.payment_info_id = cls.client.post(
                                    "/api/payment_info/", 
                                    cls.payment_data, 
                                    format="json"
                                    ).json()["id"]
        
        cls.payment_info_id_2 = cls.client.post(
                                    "/api/payment_info/", 
                                    cls.payment_data_2, 
                                    format="json"
                                    ).json()["id"]

        cls.transaction_data = {
            "seller": {
                "id": f"{cls.seller_id}",
                "products": [
                    {
                        "id": f"{cls.product_id_list[0]}",
                        "quantity": 2
                    },
                    {
                        "id": f"{cls.product_id_list[1]}",
                        "quantity": 5
                    },
                    {
                        "id": f"{cls.product_id_list[2]}",
                        "quantity": 1
                    }
                ]
            },
            "payment_info": {
                "id":  f"{cls.payment_info_id}"
            }
        }
        
        cls.transaction_data_2 = {
            "seller": {
                "id": f"{cls.seller_id_2}",
                "products": [
                    {
                        "id": f"{cls.product_id_list_2[0]}",
                        "quantity": 2
                    },
                    {
                        "id": f"{cls.product_id_list_2[1]}",
                        "quantity": 5
                    },
                    {
                        "id": f"{cls.product_id_list_2[2]}",
                        "quantity": 1
                    }
                ]
            },
            "payment_info": {
                "id":  f"{cls.payment_info_id}"
            }
        }
        
        cls.transaction_data_3 = {
            "seller": {
                "id": f"{cls.seller_id_2}",
                "products": [
                    {
                        "id": f"{cls.product_id_list_2[0]}",
                        "quantity": 2
                    },
                    {
                        "id": f"{cls.product_id_list_2[1]}",
                        "quantity": 5
                    },
                    {
                        "id": f"{cls.product_id_list_2[2]}",
                        "quantity": 1
                    }
                ]
            },
            "payment_info": {
                "id":  f"{cls.payment_info_id_2}"
            }
        }
        
        cls.transaction_wrong_data = {
            "selle": {
                "id": f"{cls.seller_id}",
                "product": [
                    {
                        "id": f"{cls.product_id_list[0]}",
                        "quantity": 2
                    },
                    {
                        "id": f"{cls.product_id_list[1]}",
                        "quantity": 5
                    },
                    {
                        "id": f"{cls.product_id_list[2]}",
                        "quantity": 1
                    }
                ]
            },
            "payment": {
                "id":  f"{cls.payment_info_id}"
            }
        }
        
        cls.error_transaction_response  = {
            "error": [
                "All products must belong to the same seller",
                "Product does not exist",
                "Product is not available",
                "Product is not active"
            ]
        }



    def test_buyer_create_transaction_success_201(self):
        # Login with buyer user 
        token = self.client.post(
            "/api/login/", self.buyer_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.post(
            "/api/transactions/", self.transaction_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", output)
        self.assertIn("amount", output)
        self.assertEqual(output["amount"], "2756.92")

    def test_buyer_create_transaction_with_wrong_fields_fail_400(self):
        # Login with buyer user 
        token = self.client.post(
            "/api/login/", self.buyer_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        response = self.client.post(
            "/api/transactions/", self.transaction_wrong_data, format="json")
        output = response.json()
        
        self.assertEqual(response.status_code, 400)
        self.assertNotIn("id", output)
        self.assertNotIn("amount", output)
        

    def test_buyer_create_transaction_fail_id_product_doesnt_belongs_to_seller(self):
        # Login with buyer user 
        token = self.client.post(
            "/api/login/", self.buyer_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        transaction_data = self.transaction_data
        transaction_data['seller']['id'] = "9561f105-0efa-4a1f-adc1-f7475b3868a4"

        response = self.client.post(
            "/api/transactions/", transaction_data, format="json")
        output = response.json()
        
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(output, self.error_transaction_response)
        
    def test_buyer_create_transaction_fail_product_id_product_doesnt_belongs_to_seller(self):
        # Login with buyer user 
        token = self.client.post(
            "/api/login/", self.buyer_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        transaction_data = self.transaction_data
        transaction_data['seller']['products'][0]['id'] = "9561f105-0efa-4a1f-adc1-f7475b3868a4"

        response = self.client.post(
            "/api/transactions/", transaction_data, format="json")
        output = response.json()
        
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(output, self.error_transaction_response)
    
    def test_buyer_create_transaction_fail_quantity_of_product_not_available(self):
        # Login with buyer user 
        token = self.client.post(
            "/api/login/", self.buyer_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        transaction_data = self.transaction_data
        transaction_data['seller']['products'][0]['quantity'] = 50

        response = self.client.post(
            "/api/transactions/", transaction_data, format="json")
        output = response.json()
        
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(output, self.error_transaction_response)
        
    def test_buyer_create_transaction_fail_payment_info_doesnt_belong_to_buyer(self):
        # Login with buyer user 
        token = self.client.post(
            "/api/login/", self.buyer_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        transaction_data = self.transaction_data
        transaction_data['payment_info']['id'] = "4005e118-75a9-4ef9-80cf-942e0911b90f"

        response = self.client.post(
            "/api/transactions/", transaction_data, format="json")
        output = response.json()
        
        self.assertEqual(response.status_code, 403)
        self.assertDictEqual(output, { "detail": "You do not have permission to perform this action." })
    
    def test_buyer_create_transaction_fail_cart_is_expired(self):
        # Login with buyer user 
        token = self.client.post(
            "/api/login/", self.buyer_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        payment_info = PaymentInfo.objects.get(id=self.payment_info_id)
        payment_info.card_expiring_date = '1900-04-01'
        payment_info.save()
        
        response = self.client.post(
            "/api/transactions/", self.transaction_data, format="json")
        output = response.json()
        
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(output, {"error": ["This card is expired"]})
    
    def test_if_the_products_have_been_decremented(self):
        # Login with buyer user 
        token = self.client.post(
            "/api/login/", self.buyer_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Realiza a transação
        self.client.post(
            "/api/transactions/", self.transaction_data, format="json")
        
        # Lists the products, the quantity must be subtracted from the transaction made
        response = self.client.get(
            "/api/products/", format="json")
        output = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertIs(output[0]['quantity'], 13)
        self.assertIs(output[1]['quantity'], 5)
        self.assertIs(output[2]['quantity'], 18)

    def test_admin_create_transaction_fail_403(self):
        # Login with admin user 
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.post(
            "/api/transactions/", self.transaction_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(output, 
            {'detail': 'You do not have permission to perform this action.'})


    def test_seller_create_transaction_fail_403(self):
        # Login with seller user 
        token = self.client.post(
            "/api/login/", self.seller_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.post(
            "/api/transactions/", self.transaction_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(output, 
            {'detail': 'You do not have permission to perform this action.'})

    def test_anonymous_create_transaction_fail_401(self):
        # No credentials
        self.client.credentials()

        response = self.client.post(
            "/api/transactions/", self.transaction_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(output, 
            {"detail": "Authentication credentials were not provided."})


    def test_seller_list_transactions_success_200(self):
        # Login with buyer user 
        token = self.client.post(
            "/api/login/", self.buyer_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create 2 transactions
        self.client.post(
            "/api/transactions/", self.transaction_data, format="json")
        
        self.client.post(
            "/api/transactions/", self.transaction_data, format="json")
        
        # Login with seller user 
        token = self.client.post(
            "/api/login/", self.seller_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # list transactions
        response = self.client.get(
            "/api/transactions/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(output), 2)

    def test_buyer_list_transactions_fail_403(self):
        # Login with buyer user 
        token = self.client.post(
            "/api/login/", self.buyer_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # list transactions
        response = self.client.get(
            "/api/transactions/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(output, {"detail": "You do not have permission to perform this action."})

    def test_admin_list_transactions_success_200(self):
        # Login with buyer user 
        token = self.client.post(
            "/api/login/", self.buyer_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create transaction seller 1
        self.client.post(
            "/api/transactions/", self.transaction_data, format="json")
        
        # create transaction seller 2
        self.client.post(
            "/api/transactions/", self.transaction_data_2, format="json")
        
        # Login with admin user 
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        response = self.client.get('/api/transactions/', format='json')
        output = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(output), 2)
        
    def test_seller_list_only_his_transactions_success_200(self):
        # Login with buyer user 
        token = self.client.post(
            "/api/login/", self.buyer_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create transaction seller 1
        self.client.post(
            "/api/transactions/", self.transaction_data, format="json")
        
        # create transaction seller 2
        self.client.post(
            "/api/transactions/", self.transaction_data_2, format="json")
        
        # Login with seller user 
        token = self.client.post(
            "/api/login/", self.seller_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        response = self.client.get('/api/transactions/', format='json')
        output = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(output), 1)

    def test_anonymous_list_transactions_fail_401(self):
        # No credentials
        self.client.credentials()
        
        response = self.client.get('/api/transactions/', format='json')
        output = response.json()
        
        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(output, {"detail": "Authentication credentials were not provided."})


    def test_seller_list_payables_success_200(self):
        # Login with buyer user 
        token = self.client.post(
            "/api/login/", self.buyer_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create 2 transactions seller 1
        # debit transaction
        self.client.post(
            "/api/transactions/", self.transaction_data, format="json")
        #  debi transaction
        self.client.post(
            "/api/transactions/", self.transaction_data, format="json")
        
        # create 2 transactions seller 2
        # debit transaction
        self.client.post(
            "/api/transactions/", self.transaction_data_2, format="json")
        # credit transaction
        self.client.post(
            "/api/transactions/", self.transaction_data_3, format="json")
        
        # Login with seller 1 user 
        token = self.client.post(
            "/api/login/", self.seller_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        response = self.client.get('/api/payables/', format='json')
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(output["payable_amount_paid"], 5348.42)
        self.assertEqual(output["payable_amount_waiting_funds"], None)
        
        # Login with seller 2 user 
        token = self.client.post(
            "/api/login/", self.seller_login_data_2, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        response = self.client.get('/api/payables/', format='json')
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(output["payable_amount_paid"], 2674.21)
        self.assertEqual(output["payable_amount_waiting_funds"], 2619.07)
        
    def test_seller_list_payables_updated_as_of_the_date_200(self):
        # Login with buyer user 
        token = self.client.post(
            "/api/login/", self.buyer_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # create 2 transactions seller 2
        # debit transaction
        transaction_1 = self.client.post(
            "/api/transactions/", self.transaction_data_2, format="json")
        # credit transaction
        transaction_2 = self.client.post(
            "/api/transactions/", self.transaction_data_3, format="json")
        
        # Login with seller 2 user 
        token = self.client.post(
            "/api/login/", self.seller_login_data_2, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        response = self.client.get('/api/payables/', format='json')
        output = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(output["payable_amount_paid"], 2674.21)
        self.assertEqual(output["payable_amount_waiting_funds"], 2619.07)
        
        payable = Payable.objects.get(transaction_id = transaction_2.json()['id'])
        payable.payment_date = "2022-01-01"
        payable.save()
        
        response = self.client.get('/api/payables/', format='json')
        output = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(output["payable_amount_paid"], 5293.28)
        self.assertEqual(output["payable_amount_waiting_funds"], None)
   

    def test_buyer_list_payables_fail_403(self):
        # Login with buyer user 
        token = self.client.post(
            "/api/login/", self.buyer_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        response = self.client.get('/api/payables/', format='json')
        output = response.json()
        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(output, {"detail": "You do not have permission to perform this action."})
        
    def test_admin_list_payables_fail_403(self):
       # Login with admin user 
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
            ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        response = self.client.get('/api/payables/', format='json')
        output = response.json()
        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(output, {"detail": "You do not have permission to perform this action."})
     
    def test_anonymous_list_payables_fail_401(self):
        # Login with anonymous user 
        self.client.credentials()
        
        response = self.client.get('/api/payables/', format='json')
        output = response.json()
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(output, {"detail": "Authentication credentials were not provided."})