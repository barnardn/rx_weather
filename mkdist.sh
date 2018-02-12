#!/bin/sh

rm dist/*

echo "Making source package..."
python3 setup.py sdist
echo "Making python3 wheel..."
python3 setup.py bdist_wheel
echo "Creating signatures..."
gpg --detach-sign -a dist/*.whl
gpg --detach-sign -a dist/*.tar.gz
echo "Done."

