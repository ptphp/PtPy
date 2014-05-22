# ----- Run tests: ------
python -m tornado.testing  discover

# ---- Run single test ------
python -m tornado.testing  tests.test_client

easy_install supervisord

supervisord -c /etc/supervisord.conf

sudo supervisorctl restart all