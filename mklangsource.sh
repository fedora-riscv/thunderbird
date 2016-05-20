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
    #hg update
    popd
  else
    hg clone -u $tag http://hg.mozilla.org/releases/l10n/mozilla-release/$lang
    #hg clone http://hg.mozilla.org/l10n-central/$lang
  fi
done
cd ..
# Need to merge by compare-locale tool
# More info here: https://developer.mozilla.org/en-US/docs/Mozilla/Projects/compare-locales
# how to get compare-locales: sudo easy_install -U compare-locales

# Make copy to merge with
rm -rf l10n-merged
cp -R l10n l10n-merged
for lang in $(<$locales)
do
  compare-locales --merge l10n-merged/$lang $PWD/thunderbird-${tbver}/${branch}/calendar/locales/l10n.ini l10n $lang
done


# Tar up, minus the mercurial files
rm -f l10n-${lver}.tar.xz
tar caf l10n-lightning-${tbver}.tar.xz --exclude='.hg*'  l10n-merged
