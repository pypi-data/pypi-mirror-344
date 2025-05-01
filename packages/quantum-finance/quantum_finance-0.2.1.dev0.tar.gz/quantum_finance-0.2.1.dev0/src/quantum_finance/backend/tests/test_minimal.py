'''
This is a minimal test file to verify that the testing framework is working.
We add extensive notation to track what we're testing and why.
'''

def test_basic_arithmetic():
    '''
    This test checks basic arithmetic as a sanity check.
    If this fails, there's likely an environment or configuration problem.
    '''
    x = 2 + 2
    assert x == 4, 'Expected 2+2 to equal 4'
 