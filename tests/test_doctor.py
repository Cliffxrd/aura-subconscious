from core.cli.doctor import AuraDoctor

def test_run_health_check():
    assert AuraDoctor.run_health_check() is True
