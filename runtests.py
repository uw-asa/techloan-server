import sys
import django
from django.conf import settings
from django.test.utils import get_runner


settings.configure(
    INSTALLED_APPS=('techloan_server',),
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3'}},
    USE_TZ=True,
)

if __name__ == "__main__":
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['techloan_server'])
    sys.exit(bool(failures))
