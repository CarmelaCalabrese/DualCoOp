#!/bin/bash

#  A script to download something something dataset, provided that you can authenticate

BASE_URL='https://developer.qualcomm.com/qfile/'
URL_QFILE=68975
BASE_OUTPUT='something-something-v2-'
OUT_DIR='something-something-v2'
COOKIE='OptanonAlertBoxClosed=2023-11-23T10:04:53.334Z; s_fid=3875BB3C49B4C5A5-1B4936EB13644AF1; INGRESSCOOKIE=1701251952.12.378.150686|b1b41e039a516dae4a16dde1372167d1; s_cc=true; s_sq=%5B%5BB%5D%5D; SESSe9b825fe435fd0ce0540e1ea73912b52=XVkl3y6OeAw2u2IskfGZ-d21XPdG7zIJm9F7ASorHG8; OneTrustActiveGroups=,C0001,; utag_main=v_id:018a600b733a0011f7ce645844c305065004705d00fb8$_sn:5$_se:15$_ss:0$_st:1701254162449$vapi_domain:qualcomm.com$ses_id:1701251965184%3Bexp-session$_pn:7%3Bexp-session; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Nov+29+2023+11%3A06%3A02+GMT%2B0100+(Central+European+Standard+Time)&version=202310.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=9fc9fa71-91af-421b-a74c-ddc0cc47d007&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0&geolocation=IT%3B42&AwaitingReconsent=false'
BASE_REFERER='https://developer.qualcomm.com/downloads/20bn-something-something-download-package-'

url() {
  echo ${BASE_URL}$1"/20bn-something-something-v2-"$2
}

referer() {
  echo ${BASE_REFERER}$1"?referrer=node/68935"
}

download_smth_smth() {
    curl "$1" \
      -H 'authority: developer.qualcomm.com' \
      -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
      -H 'accept-language: en-US,en;q=0.9' \
      -H "cookie: $COOKIE" \
      -H "referer: $REFERER" \
      -H 'sec-ch-ua: "Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"' \
      -H 'sec-ch-ua-mobile: ?0' \
      -H 'sec-ch-ua-platform: "Linux"' \
      -H 'sec-fetch-dest: document' \
      -H 'sec-fetch-mode: navigate' \
      -H 'sec-fetch-site: same-origin' \
      -H 'sec-fetch-user: ?1' \
      -H 'upgrade-insecure-requests: 1' \
      -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36' \
      --compressed \
      --output $OUT_DIR/$2
}

#Actual download template
# curl 'https://developer.qualcomm.com/qfile/68975/20bn-something-something-v2-00.zip' \
#   -H 'authority: developer.qualcomm.com' \
#   -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
#   -H 'accept-language: en-US,en;q=0.9' \
#   -H 'cookie: OptanonAlertBoxClosed=2023-11-23T10:04:53.334Z; s_fid=3875BB3C49B4C5A5-1B4936EB13644AF1; INGRESSCOOKIE=1701251952.12.378.150686|b1b41e039a516dae4a16dde1372167d1; s_cc=true; s_sq=%5B%5BB%5D%5D; SESSe9b825fe435fd0ce0540e1ea73912b52=XVkl3y6OeAw2u2IskfGZ-d21XPdG7zIJm9F7ASorHG8; OneTrustActiveGroups=,C0001,; utag_main=v_id:018a600b733a0011f7ce645844c305065004705d00fb8$_sn:6$_se:9$_ss:0$_st:1701266504887$vapi_domain:qualcomm.com$ses_id:1701262914933%3Bexp-session$_pn:5%3Bexp-session; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Nov+29+2023+14%3A31%3A45+GMT%2B0100+(Central+European+Standard+Time)&version=202310.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=9fc9fa71-91af-421b-a74c-ddc0cc47d007&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0&geolocation=IT%3B42&AwaitingReconsent=false' \
#   -H 'referer: https://developer.qualcomm.com/downloads/20bn-something-something-download-package-00?referrer=node/68935' \
#   -H 'sec-ch-ua: "Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"' \
#   -H 'sec-ch-ua-mobile: ?0' \
#   -H 'sec-ch-ua-platform: "Linux"' \
#   -H 'sec-fetch-dest: document' \
#   -H 'sec-fetch-mode: navigate' \
#   -H 'sec-fetch-site: same-origin' \
#   -H 'upgrade-insecure-requests: 1' \
#   -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36' \
#   --compressed

mkdir -p $OUT_DIR

for i in $(seq 0 19)
do

  echo $URL_QFILE
  if [[ $i -lt 10 ]]
  then
    URL=$(url $URL_QFILE "0${i}.zip")
    REFERER=$(referer "0${i}")
  else
    URL=$(url $URL_QFILE "${i}.zip")
    REFERER=$(referer "${i}")
  fi

  OUTPUT=${BASE_OUTPUT}$i.zip
  download_smth_smth $URL $OUTPUT
  let URL_QFILE=${URL_QFILE}+1

done

unzip something-something-v2-\*.zip
cat 20bn-something-something-v2-?? | tar -xvzf -
