import os
import tempfile
import unittest
import pexpect


class SimpleVersionFile(unittest.TestCase):
    def setUp(self):
        self._tempfiles = []

    def tearDown(self):
        for tmp in self._tempfiles:
            os.remove(tmp)

    def versions_file(self, version):
        with tempfile.NamedTemporaryFile(delete=False) as fd:
            fd.write(version)
            fd.flush()
            self._tempfiles.append(fd.name)
            return fd.name

    def assertFileContent(self, filename, version):
        with file(filename) as fd:
            self.assertEquals(version, fd.read())

    def test_increment_the_file_content(self):
        filename = self.versions_file('0.1.2')

        sut = pexpect.spawn('python -m releaseme increment --file=%s'
                            % filename)

        sut.expect('0.1.3', timeout=2)
        self.assertFileContent(filename, '0.1.3')

    def test_increment_the_file_content_again(self):
        filename = self.versions_file('1.2.3')

        sut = pexpect.spawn('python -m releaseme increment --file=%s'
                            % filename)

        sut.expect('1.2.4', timeout=2)
        self.assertFileContent(filename, '1.2.4')
