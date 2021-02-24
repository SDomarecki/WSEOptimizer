import os

from main import set_pwd_to_application_root


def test_set_pwd_to_application_root_validPwd_shouldChangePwdToWSEOptimizerRoot():
    set_pwd_to_application_root()

    assert 'app' in os.listdir()
