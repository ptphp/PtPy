#coding:utf-8
import unittest
from manager import HandlerTestCase

class IndexHandlerTestCase(HandlerTestCase):
    def test_index_get(self):
        response = self.get('/')
        self.assertEqual(response.code, 200)
        
    def test_index_post(self):
        data = {
                "test":"tss",
                }
        response = self.post('/',data)     
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, data['test'])
        
if __name__ == "__main__":
    #IndexHandlerTestCase().main()
    unittest.main(verbosity=2)