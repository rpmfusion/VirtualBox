VERSION=6.1.4
REL=1
RAWHIDE=33
REPOS="f32 f31 f30 el7"
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
rpmdev-bumpspec -n $VERSION -c "Update VBox to $VERSION" VirtualBox.spec
rm UserManual.pdf
spectool -g VirtualBox.spec
rfpkg new-sources ./VirtualBox-$VERSION.tar.bz2 ./UserManual.pdf
rfpkg srpm && copr-cli build sergiomb/vboxfor23 VirtualBox-$VERSION-$REL.fc$RAWHIDE.src.rpm
echo Press enter to continue; read dummy;
fi

if test $stage -le 1
then
echo STAGE 1
rfpkg ci -c && git show
echo Press enter to continue; read dummy;
rfpkg push && rfpkg build --nowait
echo Press enter to continue; read dummy;
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
