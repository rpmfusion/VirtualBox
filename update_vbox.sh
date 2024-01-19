VERSION=7.0.14
REL=1
RAWHIDE=40
REPOS="f39 f38 el9 el8"
if [ -z "$1" ]
then
      stage=0
else
      stage=$1
fi

if test $stage -le 0
then
echo STAGE 0
git checkout master
git pull
  if test $REL -eq 1
  then
    rpmdev-bumpspec -n $VERSION -c "Update VirtualBox to $VERSION" VirtualBox.spec
    rm UserManual.pdf
    spectool -g VirtualBox.spec
    # we need update sources files to avoid download the wrong UserManual.pdf
    rfpkg new-sources ./VirtualBox-$VERSION.tar.bz2 ./UserManual.pdf
    echo "checking patches"
    rfpkg prep
  fi
fi

if test $stage -le 1
then
echo STAGE 1
echo Press enter scratch-build or n to skip ; read dummy;
    if [[ "$dummy" != "n" ]]; then
        rfpkg scratch-build --srpm
    fi
echo Press enter to build on corp -build or n to skip ; read dummy;
    if [[ "$dummy" != "n" ]]; then
        rfpkg copr-build sergiomb/vboxfor23
    fi
fi

if test $stage -le 2
then
echo STAGE 2
echo Press enter to commit; read dummy;
rfpkg ci -c && git show
fi

if test $stage -le 3
then
echo STAGE 3
echo Press enter to push and build on rawhide; read dummy;
rfpkg push && rfpkg build
fi

if test $stage -le 4
then
echo STAGE 4
for repo in $REPOS ; do
echo Press enter to build on branch $repo or n to skip; read dummy;
if [[ "$dummy" != "n" ]]; then
git checkout $repo && git merge master && git push && rfpkg build; git checkout master
fi
done
fi

echo "Continue in ../VirtualBox-kmod/update_vbox.sh"
