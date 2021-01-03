import os
import unittest
import batchkit


class TestBatchKit(unittest.TestCase):
    def setUp(self):
        self.bk = batchkit.BatchKit()

    def test01_date_time(self):
        self.assertRegex(self.bk.get_date(), r'^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$')
        self.assertRegex(self.bk.get_time(), r'^([0-1][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$')

    def test02_txt_write_read(self):
        self.assertTrue(self.bk.txt_write('Test\n', 'Test.txt'))
        self.assertEqual(self.bk.txt_read('Test.txt'), 'Test\n')
        self.assertIsNone(self.bk.get_err())

    def test03_txt_append_read(self):
        self.assertTrue(self.bk.txt_append('Test2\n', 'Test.txt'))
        self.assertEqual(self.bk.txt_read('Test.txt'), 'Test\nTest2\n')
        self.assertIsNone(self.bk.get_err())

    def test04_txt_read_error(self):
        os.remove('Test.txt')
        self.assertIsNone(self.bk.txt_read('Test.txt'))

        err = self.bk.get_err()
        self.assertIsInstance(err, str)
        self.assertGreater(len(err), 0)

    def test05_runproc(self):
        self.assertTrue(self.bk.txt_write('print("Test")', 'test.py'))

        res = self.bk.run_proc('python', 'test.py')
        self.assertEqual(res['returncode'], 0)
        self.assertEqual(res['stdout'].strip(), 'Test')
        self.assertEqual(len(res['stderr']), 0)

    def test06_runproc_badresult(self):
        os.remove('test.py')
        res = self.bk.run_proc('python', 'test.py')
        self.assertEqual(res['returncode'], 2)
        self.assertEqual(len(res['stdout']), 0)
        self.assertGreater(len(res['stderr']), 0)

    def test07_runproc_error(self):
        self.assertIsNone(self.bk.run_proc('unavailable'))

        err = self.bk.get_err()
        self.assertIsInstance(err, str)
        self.assertGreater(len(err), 0)

    def test08_get_scrpath(self):
        self.assertRegex(self.bk.get_name(), r'.+batchkit\.py$')

    def test09_get_version(self):
        self.assertRegex(self.bk.get_ver(), r'^v[0-9]\.[0-9]+(-[0-9]+-\w{8,})?$')


if __name__ == '__main__':
    unittest.main(argv=[__file__, '-v'])
