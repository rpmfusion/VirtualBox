VERSION=6.1.20
REL=1
RAWHIDE=35
REPOS="f34 f33 f32 el8 el7"
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
fi
rfpkg srpm && copr-cli build sergiomb/vboxfor23 VirtualBox-$VERSION-$REL.fc$RAWHIDE.src.rpm
fi

if test $stage -le 1
then
echo STAGE 1
rfpkg ci -c && git show
echo Press enter to push and build on rawhide; read dummy;
rfpkg push && rfpkg build --nowait
fi

if test $stage -le 2
then
echo STAGE 2
for repo in $REPOS ; do
echo Press enter to build on branch $repo; read dummy;
git checkout $repo && git merge master && git push && rfpkg build --nowait; git checkout master
done
fi

echo "Continue in ../VirtualBox-kmod/update_vbox.sh"
