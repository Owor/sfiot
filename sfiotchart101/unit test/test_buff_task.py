import unittest

import sys,os

sys.path.append(os.path.join(os.path.dirname(__file__),'../lib'))
from design_buff import design_buff

test_dict_same = {'id':1,'power':123}
class TestBuffTask(unittest.TestCase):
    
    def test_normal_push(self):
        buff = design_buff()
        cases_info_diff = {
            'id':3,
            'power':333
        }
        buff.push(cases_info_diff)
        result_array = buff.show_buff()

        assert result_array[0][0] == {'id': 3, 'power': 333}

    def test_normal_pop(self):
        buff = design_buff()

        cases_info_diff = {
            'id':3,
            'power':333
        }
        buff.push(cases_info_diff)
        buff.pop()
        result_array = buff.show_buff()
        assert result_array == []
    
    # def test_push_of_lock_block_successful(self):



if __name__ == '__main__':
    unittest.main()