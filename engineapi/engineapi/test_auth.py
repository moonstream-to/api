import time
import unittest

from brownie import network, accounts
from hexbytes import HexBytes

from .auth import (
    authorize,
    verify,
    MoonstreamAuthorizationVerificationError,
    MoonstreamAuthorizationExpired,
)


class TestAuth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            network.connect()
        except:
            pass
        cls.signer = accounts.add()

        cls.non_signer = accounts.add()

    def test_authorization_and_verification(self):
        current_time = int(time.time())
        payload = authorize(
            current_time + 300, self.signer.address, HexBytes(self.signer.private_key)
        )
        self.assertDictContainsSubset(
            {"address": self.signer.address, "deadline": current_time + 300}, payload
        )
        self.assertTrue(verify(payload))

    def test_authorization_and_verification_fails_for_wrong_address(self):
        current_time = int(time.time())
        payload = authorize(
            current_time + 300, self.signer.address, HexBytes(self.signer.private_key)
        )
        payload["address"] = self.non_signer.address
        with self.assertRaises(MoonstreamAuthorizationVerificationError):
            verify(payload)

    def test_authorization_and_verification_fails_after_deadline(self):
        current_time = int(time.time())
        payload = authorize(
            current_time - 1, self.signer.address, HexBytes(self.signer.private_key)
        )
        with self.assertRaises(MoonstreamAuthorizationExpired):
            verify(payload)


if __name__ == "__main__":
    unittest.main()
