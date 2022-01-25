# Mindsync platform API for python

## Run tests

```bash
git clone git@github.com:mindsync-ai/mindsync-api-python.git
cd mindsync-api-python
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=$(pwd) pytest
```

MINDSYNC_API_KEY=fd3f74f9bfb6b9868bee9bfadfefe69d MINDSYNC_BASE_URL=https://api.mdscdev.com/swagger/ mindsync --prettify profile
mindsync --api-key fd3f74f9bfb6b9868bee9bfadfefe69d --base-url https://api.mdscdev.com/swagger/ --prettify profile