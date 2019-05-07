#!/bin/bash
#set -x
set -e
usage()
{
cat << EOF
usage: $0 options

This script downloads calendar langpacks for Thunderbird.

OPTIONS:
   -h      Show this message
   -v      Version string (7.0.1)
   -b      Build number (1, 2, 3)
   -r      Reuse downloaded files (when you don't want to redownload)
EOF
}

VER=
BUILDNUM=
LANG_DATE=`date "+%Y%m%d"`
while getopts “hv:b:r” OPTION
do
     case $OPTION in
         h)
             usage
             exit 1
             ;;
         v)
             VER=$OPTARG
             ;;
         b)
             BUILDNUM=$OPTARG
             ;;
         ?)
             usage
             exit
             ;;
     esac
done

if [ -z "$VER" -o -z "$BUILDNUM"  ]
then
     echo "Missing version or build number."
     usage
     exit 1
fi

WHITE='\033[1;33m'
NC='\033[0m' # No Color

LOCALES=`curl -f https://archive.mozilla.org/pub/thunderbird/candidates/$VER-candidates/build$BUILDNUM/linux-i686/ | grep "a href"|sed -e "s|.*/\([^/]*\)/\".*|\1|"|tail -n+2 |grep -v xpi`
#echo $LOCALES
rm -rf lightning-langpacks
mkdir -p lightning-langpacks
cd lightning-langpacks
LOCALE_COUNT=`echo $LOCALES| tr ' ' '\n' | wc -l`
LOCALE_NUM=0
for lang in $LOCALES; do
  LOCALE_NUM=$((LOCALE_NUM+1))
  echo -e "${WHITE}Processing calendar locale: $lang ($LOCALE_NUM/$LOCALE_COUNT)${NC}"
  mkdir -p extracted_lightning
  mkdir -p calendar-locales
  #echo Downloading TB binary for locale: $lang
  wget --quiet https://archive.mozilla.org/pub/thunderbird/candidates/$VER-candidates/build$BUILDNUM/linux-i686/$lang/thunderbird-$VER.tar.bz2

  cd extracted_lightning
  tar -xf ../thunderbird-$VER.tar.bz2 thunderbird/distribution/extensions/\{e2fda1a4-762b-4020-b5ad-a41df1933103\}.xpi
  set +e
  unzip -qq thunderbird/distribution/extensions/\{e2fda1a4-762b-4020-b5ad-a41df1933103\}.xpi
  set -e
  LIGHTNING_VERSION=`cat app.ini |grep "^Version="|sed -e 's/Version=//'`
  BUILD_ID=`cat app.ini |grep "^BuildID="|sed -e 's/BuildID=//'`
  MAX_VERSION=`cat app.ini |grep MaxVersion|sed -e s/MaxVersion=//`
  MIN_VERSION=`cat app.ini |grep MinVersion|sed -e s/MinVersion=//`
  rm -rf thunderbird
  mkdir -p ../calendar-locales/chrome
  cp -r chrome/calendar-$lang ../calendar-locales/chrome
  cp -r chrome/lightning-$lang ../calendar-locales/chrome
  cd -

  cd calendar-locales
  # create manifest
  cat > manifest.json <<EOL
{
  "languages": {
    "$lang": {
      "chrome_resources": {
        "calendar": "chrome/calendar-$lang/locale/$lang/calendar/",
        "lightning": "chrome/lightning-$lang/locale/$lang/lightning/"
      },
      "version": "$LIGHTNING_VERSION"
    }
  },
  "applications": {
    "gecko": {
      "strict_min_version": "$MIN_VERSION",
      "id": "langpack-cal-$lang@lightning.mozilla.org",
      "strict_max_version": "$MAX_VERSION"
    }
  },
  "langpack_id": "$lang",
  "version": "7.$LIGHTNING_VERSION.$BUILD_ID",
  "name": "$lang Language Pack Calendar",
  "manifest_version": 2,
  "sources": {
    "browser": {
      "base_path": "browser/"
    }
  },
  "author": "Mozilla.cz (contributors: Pavel Cvrček, Pavel Franc, Michal Stanke, Michal Vašíček)",
  "description": "Language pack for Thunderbird for $lang, this was repacked by Fedora/RHEL package maintainer from original binaries."
}

EOL
  zip --quiet -r ../langpack-cal-$lang@lightning.mozilla.org.xpi *
  cd -
  rm -rf calendar-locales
  rm -rf extracted_lightning

  rm -f thunderbird-$VER.tar.bz2
done
echo "Creating lightning-langpacks-$VER.tar.xz..."
tar cJf ../lightning-langpacks-$VER.tar.xz *.xpi
cd ..
rm -rf lightning-langpacks
