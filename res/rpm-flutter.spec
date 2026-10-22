Name:       hvnremotehub
Version:    2.0.0
Release:    0
Summary:    HVN Remote Hub
License:    GPL-3.0
URL:        https://hvn.vn
Vendor:     HVN GROUP <kythuat@hvn.vn>
Requires:   gtk3 libxcb libXfixes alsa-lib libva gstreamer1-plugins-base
Recommends: libayatana-appindicator-gtk3 libxdo
Provides:   libdesktop_drop_plugin.so()(64bit), libdesktop_multi_window_plugin.so()(64bit), libfile_selector_linux_plugin.so()(64bit), libflutter_custom_cursor_plugin.so()(64bit), libflutter_linux_gtk.so()(64bit), libscreen_retriever_plugin.so()(64bit), libtray_manager_plugin.so()(64bit), liburl_launcher_linux_plugin.so()(64bit), libwindow_manager_plugin.so()(64bit), libwindow_size_plugin.so()(64bit), libtexture_rgba_renderer_plugin.so()(64bit)

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
HVN Remote Hub, the remote desktop client of HVN GROUP, based on RustDesk.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

# %global __python %{__python3}

%install

mkdir -p "%{buildroot}/usr/share/hvnremotehub" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/share/hvnremotehub"
mkdir -p "%{buildroot}/usr/bin"
install -Dm 644 $HBB/res/hvnremotehub.service -t "%{buildroot}/usr/share/hvnremotehub/files"
install -Dm 644 $HBB/res/hvnremotehub.desktop -t "%{buildroot}/usr/share/hvnremotehub/files"
install -Dm 644 $HBB/res/hvnremotehub-link.desktop -t "%{buildroot}/usr/share/hvnremotehub/files"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/icons/hicolor/256x256/apps/hvnremotehub.png"
install -Dm 644 $HBB/res/scalable.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/hvnremotehub.svg"

%files
/usr/share/hvnremotehub/*
/usr/share/hvnremotehub/files/hvnremotehub.service
/usr/share/icons/hicolor/256x256/apps/hvnremotehub.png
/usr/share/icons/hicolor/scalable/apps/hvnremotehub.svg
/usr/share/hvnremotehub/files/hvnremotehub.desktop
/usr/share/hvnremotehub/files/hvnremotehub-link.desktop

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
ln -sf /usr/share/hvnremotehub/hvnremotehub /usr/bin/hvnremotehub
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
    rm /usr/bin/hvnremotehub || true
    rmdir /usr/lib/hvnremotehub || true
    rmdir /usr/local/hvnremotehub || true
    rmdir /usr/share/hvnremotehub || true
    rm /usr/share/applications/hvnremotehub.desktop || true
    rm /usr/share/applications/hvnremotehub-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
    rmdir /usr/lib/hvnremotehub || true
    rmdir /usr/local/hvnremotehub || true
  ;;
esac
