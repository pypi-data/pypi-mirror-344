SCRIPT_DIR=$(dirname $0)

cd $SCRIPT_DIR/..

python -m build
python3 -m twine upload dist/*
