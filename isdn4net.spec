Summary:	Networking with the isdn subsystem
Name:		isdn4net
Version:	1.4.6
Release:	23
License:	GPLv2
Group:		System/Kernel and hardware
Url:		http://www.isdn4net.berlios.de
Source0:	%{name}-%{version}.tar.bz2
Patch0:         isdn4net-1.4.6-isdnlog.patch
Patch1:         isdn4net-1.4.6-dialmode.patch
Patch2:         isdn4net-1.4.6-init-typo-fixes.patch
Patch3:         isdn4net-1.4.6-dial-on-ifup.patch
Patch4:         isdn4net-multiple-cards.diff
Patch5:         isdn4net-1.4.6-fix-link-remove-bug.diff
Patch6:         isdn4net-1.4.6-create-devices.patch
BuildArch:	noarch
Requires(post,preun): rpm-helper
Conflicts:	isdn-light

%description
This package provides several scripts to do networking with isdn4linux, several
sample configurations for card and ippp setup and small configuration and
admin utility.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p0 -b .typos
%patch3 -p0
%patch4 -p0
%patch5 -p1
%patch6 -p1 -b .udev

%install
install -d %{buildroot}/%{_sysconfdir}/sysconfig/network-scripts
install network-scripts/ifup-ippp %{buildroot}/%{_sysconfdir}/sysconfig/network-scripts
install network-scripts/ifdown-ippp %{buildroot}/%{_sysconfdir}/sysconfig/network-scripts
install network-scripts/ifup-isdn %{buildroot}/%{_sysconfdir}/sysconfig/network-scripts
install network-scripts/ifdown-isdn %{buildroot}/%{_sysconfdir}/sysconfig/network-scripts

install -d %{buildroot}/%{_initrddir}
install -m0755 init.d/isdn4linux %{buildroot}/%{_initrddir}
install -m0755 init.d/isdnlog %{buildroot}/%{_initrddir}

install -d %{buildroot}/%{_sysconfdir}/sysconfig
install defaults/isdn %{buildroot}/%{_sysconfdir}/sysconfig/isdn

install -d %{buildroot}/%{_sysconfdir}/isdn/profile
install -m 644 defaults/ippp.default %{buildroot}/%{_sysconfdir}/isdn/profile/ippp.default
install -m 644 defaults/isdn.default %{buildroot}/%{_sysconfdir}/isdn/profile/isdn.default
install -m 644 defaults/isdn.map %{buildroot}/%{_sysconfdir}/isdn/profile/isdn.map
install -m 644 defaults/ippp.map %{buildroot}/%{_sysconfdir}/isdn/profile/ippp.map

install -d %{buildroot}/%{_sysconfdir}/isdn/profile/card
install -m 644 defaults/mycard %{buildroot}/%{_sysconfdir}/isdn/profile/card/mycard

install -d %{buildroot}/%{_sysconfdir}/isdn/profile/link
install -m 644 defaults/myisp %{buildroot}/%{_sysconfdir}/isdn/profile/link/myisp
install -m 644 defaults/my_isdnlog.conf %{buildroot}/%{_sysconfdir}/isdn/my_isdnlog.conf

install -d %{buildroot}/%{_sysconfdir}/isdn/budget
# Install frontend
install -d %{buildroot}/%{_bindir}
install bin/isdn %{buildroot}/%{_bindir}/isdn

%post
echo -n "Activating isdn4linux card init:"
%_post_service isdn4linux
%_post_service isdnlog
echo " done."

%preun
echo -n "Deactivating isdn4linux card init:"
%_preun_service isdn4linux
%_preun_service isdnlog
echo " done."

%files
%config(noreplace) %{_sysconfdir}/sysconfig/network-scripts/ifup-ippp
%config(noreplace) %{_sysconfdir}/sysconfig/network-scripts/ifdown-ippp
%config(noreplace) %{_sysconfdir}/sysconfig/network-scripts/ifup-isdn
%config(noreplace) %{_sysconfdir}/sysconfig/network-scripts/ifdown-isdn
%{_initrddir}/isdn4linux
%{_initrddir}/isdnlog
%{_bindir}/isdn
%config(noreplace) %{_sysconfdir}/sysconfig/isdn
%config(noreplace) %{_sysconfdir}/isdn/profile/ippp.default
%config(noreplace) %{_sysconfdir}/isdn/profile/isdn.default
%config(noreplace) %{_sysconfdir}/isdn/profile/ippp.map
%config(noreplace) %{_sysconfdir}/isdn/profile/isdn.map
%config(noreplace) %{_sysconfdir}/isdn/profile/link/myisp
%config(noreplace) %{_sysconfdir}/isdn/profile/card/mycard
%config(noreplace) %{_sysconfdir}/isdn/my_isdnlog.conf
%doc defaults
%doc samples
%doc doc
%doc README
%dir %{_sysconfdir}/isdn/profile
%dir %{_sysconfdir}/isdn/profile/link
%dir %{_sysconfdir}/isdn/profile/card
%dir %{_sysconfdir}/isdn/budget

