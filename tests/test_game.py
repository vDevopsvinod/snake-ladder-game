import unittest
from src.game import get_new_position

class TestSnakeLadder(unittest.TestCase):
    def test_snake(self):
        self.assertEqual(get_new_position(15, 1), 6)
    
    def test_ladder(self):
        self.assertEqual(get_new_position(1, 1), 38)
    
    def test_normal_move(self):
        self.assertEqual(get_new_position(3, 1), 4)

if __name__ == '__main__':
    unittest.main()
