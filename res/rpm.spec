Name:       hvnremotehub
Version:    2.0.0
Release:    0
Summary:    HVN Remote Hub
License:    GPL-3.0
URL:        https://hvn.vn
Vendor:     HVN GROUP <kythuat@hvn.vn>
Requires:   gtk3 libxcb libXfixes alsa-lib libva2 gstreamer1-plugins-base
Recommends: libayatana-appindicator-gtk3 libxdo

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
HVN Remote Hub, the remote desktop client of HVN GROUP, based on RustDesk.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%global __python %{__python3}

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/share/hvnremotehub/
mkdir -p %{buildroot}/usr/share/hvnremotehub/files/
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps/
mkdir -p %{buildroot}/usr/share/icons/hicolor/scalable/apps/
install -m 755 $HBB/target/release/rustdesk %{buildroot}/usr/bin/hvnremotehub
install $HBB/libsciter-gtk.so %{buildroot}/usr/share/hvnremotehub/libsciter-gtk.so
install $HBB/res/hvnremotehub.service %{buildroot}/usr/share/hvnremotehub/files/
install $HBB/res/128x128@2x.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/hvnremotehub.png
install $HBB/res/scalable.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/hvnremotehub.svg
install $HBB/res/hvnremotehub.desktop %{buildroot}/usr/share/hvnremotehub/files/
install $HBB/res/hvnremotehub-link.desktop %{buildroot}/usr/share/hvnremotehub/files/

%files
/usr/bin/hvnremotehub
/usr/share/hvnremotehub/libsciter-gtk.so
/usr/share/hvnremotehub/files/hvnremotehub.service
/usr/share/icons/hicolor/256x256/apps/hvnremotehub.png
/usr/share/icons/hicolor/scalable/apps/hvnremotehub.svg
/usr/share/hvnremotehub/files/hvnremotehub.desktop
/usr/share/hvnremotehub/files/hvnremotehub-link.desktop
/usr/share/hvnremotehub/files/__pycache__/*

%changelog
# let's skip this for now

%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop hvnremotehub || true
  ;;
esac

%post
cp /usr/share/hvnremotehub/files/hvnremotehub.service /etc/systemd/system/hvnremotehub.service
cp /usr/share/hvnremotehub/files/hvnremotehub.desktop /usr/share/applications/
cp /usr/share/hvnremotehub/files/hvnremotehub-link.desktop /usr/share/applications/
systemctl daemon-reload
systemctl enable hvnremotehub
systemctl start hvnremotehub
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop hvnremotehub || true
    systemctl disable hvnremotehub || true
    rm /etc/systemd/system/hvnremotehub.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/share/applications/hvnremotehub.desktop || true
    rm /usr/share/applications/hvnremotehub-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
