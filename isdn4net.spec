Summary:	Networking with the isdn subsystem
Name:		isdn4net
Version:	1.4.6
Release:	%mkrel 23
License:	GPL
Group:		System/Kernel and hardware
URL:		http://www.isdn4net.berlios.de
Source0:	%{name}-%{version}.tar.bz2
Patch0:         isdn4net-1.4.6-isdnlog.patch
Patch1:         isdn4net-1.4.6-dialmode.patch
Patch2:         isdn4net-1.4.6-init-typo-fixes.patch
Patch3:         isdn4net-1.4.6-dial-on-ifup.patch
Patch4:         isdn4net-multiple-cards.diff
Patch5:         isdn4net-1.4.6-fix-link-remove-bug.diff
Patch6:         isdn4net-1.4.6-create-devices.patch
BuildArch:	noarch
Requires(post): rpm-helper
Requires(preun): rpm-helper
Conflicts:	isdn-light
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
rm -fr %{buildroot}

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

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root)
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




%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.6-21mdv2011.0
+ Revision: 665527
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4.6-20mdv2011.0
+ Revision: 605987
- rebuild

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4.6-19mdv2010.1
+ Revision: 520135
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.4.6-18mdv2010.0
+ Revision: 425391
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 1.4.6-17mdv2009.1
+ Revision: 351259
- rebuild

* Tue Aug 05 2008 Olivier Blin <oblin@mandriva.com> 1.4.6-16mdv2009.0
+ Revision: 263847
- do not provide default ifcfg-ippp0, it is already written by config
  tools and the installation of this package should not make an
  unconfigured connection started at boot

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 1.4.6-15mdv2009.0
+ Revision: 221646
- rebuild

* Sun Jan 13 2008 Thierry Vignaud <tv@mandriva.org> 1.4.6-14mdv2008.1
+ Revision: 150345
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot


* Sat Mar 17 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4.6-13mdv2007.1
+ Revision: 145394
- Import isdn4net

* Sat Mar 17 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4.6-13mdv2007.1
- use the %%mrel macro
- bunzip patches

* Tue Sep 14 2004 Olivier Blin <blino@mandrake.org> 1.4.6-12mdk
- fix typo in Patch6

* Fri Sep 10 2004 Olivier Blin <blino@mandrake.org> 1.4.6-11mdk
- from Steffen Barszus <st_barszus@gmx.de>:
  o Patch6: create isdn devices when devfs isn't used

* Thu Sep 09 2004 Olivier Blin <blino@mandrake.org> 1.4.6-10mdk
- from Steffen Barszus <st_barszus@gmx.de>:
  o Patch5: fix isdn link remove (use temporary file)

* Fri Jul 23 2004 Olivier Blin <blino@mandrake.org> 1.4.6-9mdk
- add patch3 to support the DIAL_ON_IFUP variable

* Wed Jul 14 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.4.6-8mdk
- from Steffen Barszus <st_barszus@gmx.de>:
	o patch 4: multiple card handling (all files in /etc/isdn/profile/card/ are
	o considered being card configuration files)
	o remove patch 3, this isn't the right way

* Sat Jun 05 2004 Damien Chaumette <dchaumette@mandrakesoft.com> 1.4.6-7mdk
- patch 3: start connection without internet service

