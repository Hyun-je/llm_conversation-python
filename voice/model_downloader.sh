BASE_URL="https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/$1/$2/$3"
ONNX_FILE="$1-$2-$3.onnx"
JSON_FILE="$1-$2-$3.onnx.json"

if [ -e $ONNX_FILE ] ; then
    echo "$ONNX_FILE file exist"
else
    wget $BASE_URL/$ONNX_FILE
fi

if [ -e $JSON_FILE ] ; then
    echo "$JSON_FILE file exist"
else
    wget $BASE_URL/$JSON_FILE
fi