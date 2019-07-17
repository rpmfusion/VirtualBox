VERSION=6.0.10
REL=1
RAWHIDE=31
if [ -z "$1" ]
then
      stage=0
else
      stage=$1
fi

if test $stage -le 0
then
echo STAGE 0
git pull
rpmdev-bumpspec -n $VERSION -c "Update VBox to $VERSION" VirtualBox.spec
rm UserManual.pdf
spectool -g VirtualBox.spec
rfpkg srpm && copr-cli build sergiomb/vboxfor23 VirtualBox-$VERSION-$REL.fc$RAWHIDE.src.rpm
echo Press enter to continue; read dummy;
fi

if test $stage -le 1
then
echo STAGE 1
rfpkg new-sources ./VirtualBox-$VERSION.tar.bz2 ./UserManual.pdf
rfpkg ci -c && git show
echo Press enter to continue; read dummy;
rfpkg push && rfpkg build --nowait
echo Press enter to continue; read dummy;
fi

if test $stage -le 2
then
echo STAGE 2
git checkout f30 && git merge master && git push && rfpkg build --nowait; git checkout master
echo Press enter to continue; read dummy;
git checkout f29 && git merge master && git push && rfpkg build --nowait; git checkout master
echo Press enter to continue; read dummy;
git checkout f28 && git merge master && git push && rfpkg build --nowait; git checkout master
echo Press enter to continue; read dummy;
git checkout el7 && git merge master && git push && rfpkg build --nowait; git checkout master
fi

cd ../VirtualBox-kmod/
if test $stage -le 5
then
echo STAGE 5
git pull
rpmdev-bumpspec -n $VERSION -c "Update VBox to $VERSION" VirtualBox-kmod.spec
rfpkg srpm && copr-cli build sergiomb/vboxfor23 VirtualBox-kmod-$VERSION-$REL.fc$RAWHIDE.src.rpm
echo Continue in ..../VirtualBox-kmod/update_vbox.sh
