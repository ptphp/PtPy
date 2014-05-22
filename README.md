PtPy2014
========

	__method = "METHOD"
    def loadTestsFromTestCase(self, testCaseClass):
        
        """Return a suite of all tests cases contained in testCaseClass"""
        if issubclass(testCaseClass, suite.TestSuite):
            raise TypeError("Test cases should not be derived from TestSuite." \
                                " Maybe you meant to derive from TestCase?")
        testCaseNames = self.getTestCaseNames(testCaseClass)
        
        #=======================================================================
        # fix single test
        #=======================================================================        
        if testCaseNames:            
            if self.__method in os.environ.keys() and os.environ[self.__method] and os.environ[self.__method] in  testCaseNames:                
                testCaseNames = [os.environ[self.__method]]            
            
        if not testCaseNames and hasattr(testCaseClass, 'runTest'):
            testCaseNames = ['runTest']
    
        loaded_suite = self.suiteClass(map(testCaseClass, testCaseNames))
        
        return loaded_suite