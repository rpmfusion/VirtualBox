VERSION=6.1.0
REL=1
RAWHIDE=32
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
git checkout f31 && git merge master && git push && rfpkg build --nowait; git checkout master
echo Press enter to continue; read dummy;
git checkout f30 && git merge master && git push && rfpkg build --nowait; git checkout master
echo Press enter to continue; read dummy;
fi
if test $stage -le 3
then
echo STAGE 3
git checkout f29 && git merge master && git push && rfpkg build --nowait; git checkout master
fi
echo Press enter to continue; read dummy;
git checkout el7 && git merge master && git push && rfpkg build --nowait; git checkout master

echo "Continue in ../VirtualBox-kmod/update_vbox.sh"
