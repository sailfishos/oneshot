# we can't use %include for files in the source tarballs, so redefine the macros for now
%define _oneshotdir %{_libdir}/oneshot.d
%define _default_uid %(grep "^UID_MIN" /etc/login.defs |  tr -s " " | cut -d " " -f2)
%define _system_groupadd() getent group %{1} >/dev/null || groupadd -r %{1}

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
Requires(pre): /usr/bin/getent, /usr/sbin/groupadd
Requires: /usr/bin/getent, /bin/ln, /bin/touch, /bin/sed, /bin/grep, /usr/sbin/usermod
Requires: /etc/login.defs

%description
%{summary}.

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/rpm/*
%attr (755, -, -) %{_bindir}/*
%{_sysconfdir}/oneshot.d/
%dir %{_sysconfdir}/oneshot.d/
%dir %{_sysconfdir}/oneshot.d/0
%dir %{_sysconfdir}/oneshot.d/0/late
%dir %attr(775, -, oneshot) %{_sysconfdir}/oneshot.d/default/
%dir %attr(775, -, oneshot) %{_sysconfdir}/oneshot.d/default/late
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

%pre
%_system_groupadd oneshot

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

install -d %{buildroot}%{_sysconfdir}/oneshot.d/0/late
install -d %{buildroot}%{_sysconfdir}/oneshot.d/default/late
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
ln -sf ./default %{buildroot}%{_sysconfdir}/oneshot.d/%{_default_uid}


%post
%{_bindir}/groupadd-user oneshot
