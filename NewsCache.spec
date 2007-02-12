# TODO:	- review i and tests (especially .inet).
#	- review permissions for newscache.auth
#
%define		_rc	rc6
%define		_rel	0.1
Summary:	News Cache
Summary(pl.UTF-8):   nisza dla newsów
Name:		NewsCache
Version:	1.2
Release:	0.%{_rc}.%{_rel}
Epoch:		0
License:	GPL
Group:		Applications/News
Source0:	http://www.linuxhacker.at/linux/downloads/src/%{name}-%{version}%{_rc}.tar.gz
# Source0-md5:	a7b33314cd7701564b4947ab8615dcc2
Source1:	%{name}.init
Source2:	%{name}.inet
# http://www.linuxhacker.at/linux/downloads/src/NewsCache-1.2rc6-patch1.gz
Patch0:		%{name}-1.2rc6_maintainer.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-info.patch
URL:		http://www.linuxhacker.at/newscache/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libwrap-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	socket++-devel
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}

%description
NewsCache is a free cache server for USENET News. NewsCache acts to
news reading clients like a news server, except that it stores only
those articles that have been requested by at least one client.
NewsCache targets problems of the current News System like network
bandwidth consumption or the IO load caused by news clients.

%description -l pl.UTF-8
NewsCache to wolnodostępny serwer keszujący dla sieci USENET.
NewsCache jest widziany jako serwer nntp, ale przechowuje tylko te
artykuły, o które pytał choć jeden klient. NewsCache rozwiązuje
problemy takie jak zajmowanie pasma czy obciążenie systemu We/Wy
spowodowane obsługą klientów news.

%package standalone
Summary:	NewsCache standalone mode
Summary(pl.UTF-8):   NewsCache w trybie samodzielnym
Group:		Applications/News
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts
Obsoletes:	NewsCache-inetd

%description standalone
Run NewsCache in the standalone mode.

%description standalone -l pl.UTF-8
Uruchamia NewsCache w trybie samodzielnym.

%package inetd
Summary:	NewsCache inetd mode
Summary(pl.UTF-8):   NewsCache w trybie inetd
Group:		Applications/News
Requires:	%{name} = %{version}-%{release}
Requires:	rc-inetd
Obsoletes:	NewsCache-standalone

%description inetd
Run NewsCache from the inetd.

%description inetd -l pl.UTF-8
Uruchamia NewsCache pod konrolą inetd.

%prep
%setup -q -n %{name}-%{version}%{_rc}
%patch0 -p0
%patch1 -p1
%patch2 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/var/cache/newscache
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/newscache
install -D %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/newscache
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/newscache.auth{-dist,}
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/newscache.conf{-dist,}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 152 newscache
%useradd -u 152 -d /var/cache/newscache -s /bin/false -c "NewsCache User" -g newscache newscache

%postun
if [ "$1" = "0" ]; then
	%userremove newscache
	%groupremove newscache
fi

%triggerun -- %{name} < 1.2
if [ "$1" -ge "2" -a "$2" = "1" ] ; then
echo '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
%{name} works now with newscache user and group - making:
1. appropriate changes in your %{_sysconfdir}/newscache.conf ...'

%{__sed} -i -e 's@\(Username\)\s\+news@\1 newscache@' %{_sysconfdir}/newscache.conf
%{__sed} -i -e 's@\(Groupname\)\s\+news@\1 newscache@' %{_sysconfdir}/newscache.conf

echo '2. setting new, correct owner and group for /var/cache/newscache ...'

%{__chown} -R newscache:newscache /var/cache/newscache

echo 'Done.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
fi

%post standalone
/sbin/chkconfig --add newscache
%service newscache restart "NewsCache daemon"

%preun standalone
if [ "$1" = "0" ]; then
	%service newscache stop
	/sbin/chkconfig --del newscache
fi

%post inetd
%service -q rc-inetd reload

%postun inetd
if [ "$1" = "0" ]; then
	%service -q rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%doc %{_infodir}/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
%dir %attr(755,newscache,newscache) /var/cache/newscache
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
# ... or review permissions (newscache.auth contain passwords) & effects:
#%%attr(640,root,news) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/newscache.auth
#%%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/newscache.conf

%files inetd
%defattr(644,root,root,755)
%attr(640,root,root) /etc/sysconfig/rc-inetd/newscache

%files standalone
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/newscache
