# we can't use %include for files in the source tarballs, so redefine the macros for now
%define _oneshotdir %{_libdir}/oneshot.d

Name: oneshot
Version: 0.3.1
Release: 1
Summary: Hooks run on first start
BuildArch: noarch
Group: System/Base
License: GPLv2+
Source0: %{name}-%{version}.tar.gz
URL: https://git.merproject.org/mer-core/oneshot
BuildRequires: grep, systemd
Requires: systemd-user-session-targets
Requires(pre): glibc-common
Requires(pre): shadow-utils
Requires(pre): sailfish-setup >= 0.1.11
Requires: sailfish-setup >= 0.1.11
Requires: glibc-common
Requires: sed
Requires: grep
Requires: shadow-utils
Requires: coreutils
Requires: findutils
Requires: systemd

%description
%{summary}.

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/rpm/*
%attr (755, -, -) %{_bindir}/*
%{_sysconfdir}/oneshot.d/
%dir %{_sysconfdir}/oneshot.d/
%dir %{_sysconfdir}/oneshot.d/group.d
%dir %{_sysconfdir}/oneshot.d/preinit
%dir %{_oneshotdir}
%attr (755, -, -) %{_oneshotdir}/*
%{_libdir}/systemd/user/oneshot-user.service
%{_libdir}/systemd/user/oneshot-user-late.service
%{_libdir}/systemd/user/pre-user-session.target.wants/oneshot-user.service
%{_libdir}/systemd/user/post-user-session.target.wants/oneshot-user-late.service
%{_unitdir}/oneshot-root.service
%{_unitdir}/oneshot-root-late.service
%{_unitdir}/multi-user.target.wants/oneshot-root.service
%{_unitdir}/graphical.target.wants/oneshot-root-late.service

%prep
%setup -q

%build

%install
install -d %{buildroot}%{_bindir}/
install -m 755 scripts/* %{buildroot}%{_bindir}/

install -d %{buildroot}%{_unitdir}/
install -m 644 services/* %{buildroot}%{_unitdir}/

install -d %{buildroot}%{_libdir}/systemd/user/
install -m 644 services.usersession/* %{buildroot}%{_libdir}/systemd/user/

install -d %{buildroot}%{_oneshotdir}/
install -m 755 oneshot.d/* %{buildroot}%{_oneshotdir}/

install -d %{buildroot}/etc/rpm/
install -m 644 macros/* %{buildroot}/etc/rpm/

install -d %{buildroot}%{_sysconfdir}/oneshot.d/group.d/
install -d %{buildroot}%{_sysconfdir}/oneshot.d/preinit/

install -d %{buildroot}%{_unitdir}/multi-user.target.wants
install -d %{buildroot}%{_unitdir}/graphical.target.wants
install -d %{buildroot}%{_libdir}/systemd/user/pre-user-session.target.wants
install -d %{buildroot}%{_libdir}/systemd/user/post-user-session.target.wants
ln -sf ../oneshot-root.service %{buildroot}%{_unitdir}/multi-user.target.wants/
ln -sf ../oneshot-root-late.service %{buildroot}%{_unitdir}/graphical.target.wants/
ln -sf ../oneshot-user.service %{buildroot}%{_libdir}/systemd/user/pre-user-session.target.wants/
ln -sf ../oneshot-user-late.service %{buildroot}%{_libdir}/systemd/user/post-user-session.target.wants/

