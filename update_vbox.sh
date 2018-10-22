VERSION=5.2.20
REL=1
RAWHIDE=30
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
spectool -g VirtualBox.spec
rfpkg srpm && copr-cli build sergiomb/vboxfor23 VirtualBox-$VERSION-$REL.fc$RAWHIDE.src.rpm
echo Press enter to continue; read dummy;
fi

if test $stage -le 1
then
echo STAGE 1
rfpkg new-sources ./VirtualBox-$VERSION.tar.bz2
rfpkg ci -c && git show
echo Press enter to continue; read dummy;
rfpkg push && rfpkg build --nowait
echo Press enter to continue; read dummy;
fi

if test $stage -le 2
then
echo STAGE 2
git checkout f29 && git merge master && git push && rfpkg build --nowait; git checkout master
echo Press enter to continue; read dummy;
git checkout f28 && git merge master && git push && rfpkg build --nowait; git checkout master
echo Press enter to continue; read dummy;
git checkout f27 && git merge master && git push && rfpkg build --nowait; git checkout master
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
rfpkg ci -c && git show
#cp VirtualBox-kmod.spec VirtualBox-kmod.spec.new
#git reset HEAD~1
#git rm kernel-4.10.0-0.rc5.lnkops.v2.patch
echo Press enter to continue; read dummy;
rfpkg push && rfpkg build --nowait

echo Press enter to continue; read dummy;
#koji-rpmfusion watch-task
koji-rpmfusion tag-build f27-free-override VirtualBox-$VERSION-$REL.fc27
koji-rpmfusion wait-repo f27-free-build --build=VirtualBox-$VERSION-$REL.fc27
git checkout f27 && git merge master && git push && rfpkg build --nowait; git checkout master
echo Press enter to continue; read dummy;
koji-rpmfusion tag-build f26-free-override VirtualBox-$VERSION-$REL.fc26

echo "koji-rpmfusion tag-build f26-free-override VirtualBox-$VERSION-$REL.fc26
koji-rpmfusion wait-repo f26-free-build --build=VirtualBox-$VERSION-$REL.fc26
git checkout f26 && git merge master && git push && rfpkg build --nowait; git checkout master
Press enter to continue; read dummy;
koji-rpmfusion tag-build f25-free-override VirtualBox-$VERSION-$REL.fc25
koji-rpmfusion wait-repo f25-free-build --build=VirtualBox-$VERSION-$REL.fc25
git checkout f25 && git merge master && git push && rfpkg build --nowait; git checkout master
Press enter to continue; read dummy;
koji-rpmfusion tag-build el7-free-override VirtualBox-$VERSION-$REL.el7
koji-rpmfusion wait-repo el7-free-build --build=VirtualBox-$VERSION-$REL.el7
git checkout el7 && git merge master && git push && rfpkg build --nowait; git checkout master"
fi
