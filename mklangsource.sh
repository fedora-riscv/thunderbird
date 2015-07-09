#!/bin/bash
# This checks out and builds the language sources.  The lightning source needs
# to already be unpacked
#lver=`awk '/^%global *lightning_ver/ { print $3; exit }' thunderbird.spec`
tbver=`awk '/^Version:/ { print $2; exit }' thunderbird.spec`
#tag=CALENDAR_${lver//./_}_RELEASE
tag=THUNDERBIRD_${tbver//./_}_RELEASE
branch=`awk '/^%define *tarballdir/ { print $3; exit }' thunderbird.spec`
locales=$PWD/thunderbird-${tbver}/${branch}/calendar/locales/shipped-locales
#locales=$PWD/shipped-locales
if [ ! -f $locales ]
then
  echo "ERROR: missing $locales, try fedpkg prep first"
  exit 1
fi
[ ! -d l10n ] && mkdir l10n
cd l10n
for lang in $(<$locales)
do
  if [ -d $lang ]
  then
    pushd $lang
    hg pull
    hg update $tag
    popd
  else
    hg clone -u $tag http://hg.mozilla.org/releases/l10n/mozilla-release/$lang
  fi
done

# Tar up, minus the mercurial files
cd ..
rm -f l10n-${lver}.tar.xz
tar caf l10n-lightning-${tbver}.tar.xz --exclude='.hg*'  l10n
