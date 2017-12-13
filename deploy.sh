#!/usr/bin/env bash

TEMPLATE_DIR="/tmp/"
APP_NAME="multiplication-test-generator"
AWS_PROFILE_NAME="jakub"

if [ -z ${S3_BUCKET_NAME:-} ] ; then
    S3_BUCKET_NAME="jakub-zeman-voicebow-cz-multiplication"
    echo "S3_BUCKET_NAME not specified - defaulting to '${S3_BUCKET_NAME}'."
fi

if [ -z ${AWS_REGION:-} ] ; then
    AWS_REGION=eu-central-1
    echo "AWS_REGION not specified - defaulting to '${AWS_REGION}'."
fi

CURR_DIR="`pwd`"

mkdir -p "${TEMPLATE_DIR}${APP_NAME}"
cp multiplication-test-generator.py "${TEMPLATE_DIR}${APP_NAME}"
cp -a templates "${TEMPLATE_DIR}${APP_NAME}"
cp zappa_settings.template "${TEMPLATE_DIR}${APP_NAME}/zappa_settings.json"

sed -i.bak "s/%s3bucket%/${S3_BUCKET_NAME}/g" "${TEMPLATE_DIR}${APP_NAME}/zappa_settings.json"
sed -i.bak "s/%region%/${AWS_REGION}/g" "${TEMPLATE_DIR}${APP_NAME}/zappa_settings.json"
sed -i.bak "s/%appname%/${APP_NAME}/g" "${TEMPLATE_DIR}${APP_NAME}/zappa_settings.json"

cd "/tmp/${APP_NAME}"

if [ -d /tmp/${APP_NAME}/env ] ; then
    . ./env/bin/activate
else
    virtualenv env
    . ./env/bin/activate
    pip3 install zappa
    pip3 install -r "${CURR_DIR}/requirements.txt"
fi

if ./env/bin/zappa status ${AWS_PROFILE_NAME} > /dev/null 2> /dev/null ; then
    ./env/bin/zappa update ${AWS_PROFILE_NAME}
else
    ./env/bin/zappa deploy ${AWS_PROFILE_NAME}
fi
deactivate

cd "${CURR_DIR}"