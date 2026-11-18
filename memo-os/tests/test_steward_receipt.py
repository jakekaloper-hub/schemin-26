import hashlib,hmac,json,os,unittest
from unittest.mock import patch
from steward_receipt import verify

class SignedSteward(unittest.TestCase):
    def setUp(self):
        self.key='test-only-steward-verification-secret-123456789'
        self.env=patch.dict(os.environ,{'MEMO_STEWARD_VERIFICATION_KEY':self.key,
            'MEMO_TRUSTED_STEWARD_PRINCIPAL':'real-steward', 'MEMO_TRUSTED_STEWARD_VERIFIER':'trusted-idp'})
        self.env.start();self.addCleanup(self.env.stop)
        self.payload={'receiver_id':'real-steward','verification_method':'trusted-idp','state':'VALIDATED'}
    def signed(self):
        return {'payload':self.payload.copy(),'signature':hmac.new(self.key.encode(),json.dumps(self.payload,sort_keys=True,separators=(',', ':'),ensure_ascii=False).encode(),hashlib.sha256).hexdigest()}
    def test_valid_signature(self): self.assertEqual(verify(self.signed()),self.payload)
    def test_tampered_payload(self):
        x=self.signed();x['payload']['state']='REJECTED'
        with self.assertRaises(ValueError):verify(x)
    def test_wrong_principal(self):
        self.payload['receiver_id']='impersonator'
        with self.assertRaises(ValueError):verify(self.signed())
    def test_unconfigured_key(self):
        with patch.dict(os.environ,{'MEMO_STEWARD_VERIFICATION_KEY':''}):
            with self.assertRaises(ValueError):verify(self.signed())
if __name__=='__main__':unittest.main()
