Summary:	News Cache
Summary(pl):	nisza dla newsów
Name:		NewsCache
Version:	1.1.92
Release:	1
Epoch:		0
License:	GPL
Group:		Applications/News
Source0:	http://www.hstraub.at/linux/downloads/src/%{name}-%{version}.tar.gz
Source1:	%{name}-init
# Source0-md5:	8cd84c15429fbf70b9f24ab877387ab3
Patch0:		%{name}-ac_no_debug_flag_hack.patch
# http://cmeerw.org/debian/
# Patch1:		newscache_1.1.92-0cmeerw.diff.gz
# http://download.cmeerw.net/debian/newscache/source/newscache_1.1.92-0cmeerw.diff.gz
URL:		http://members.aon.at/hstraub/linux/newscache
BuildRequires:	socket++-devel
BuildRequires:	libwrap-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}

%description
NewsCache is a free cache server for USENET News. NewsCache acts to
news reading clients like a news server, except that it stores only
those articles that have been requested by at least one client.
NewsCache targets problems of the current News System like network
bandwidth consumption or the IO load caused by news clients.

%description -l pl
NewsCache to wolnodostêpny serwer keszuj±cy dla sieci USENET.
NewsCache jest widziany jako serwer nntp, ale przechowuje tylko te
artyku³y o które czya³ choæ jeden klient. NewsCache rozwi±zuje
problemy takie jak zajmowanie pasma czy obci±¿enie systemu We/Wy
spowodowane obs³ug± klientów news.

%package standalone
Summary:	NewsCache standalone mode
Summary(pl):	NewsCache w trybie samodzielnym
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Conflicts:	%{name}-inetd

%description standalone
Run NewsCache in the Standalone mode

%description standalone -l pl
Uruchamia NewsCache w trybie Standalone

%package inetd
Summary:	NewsCache inetd mode
Summary(pl):	NewsCache w trybie inetd
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	rc-inetd
Conflicts:	%{name}-inetd

%description inetd
Run NewsCache from the inetd.

%description inetd -l pl
Uruchamia NewsCache pod konrol± inetd

%prep
%setup -q
%patch0 -p0
#%patch1 -p1

%build
%define specflags '-O0'
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure	\
--enable-notcached
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
DESTDIR=$RPM_BUILD_ROOT
install -d	$RPM_BUILD_ROOT{/var/cache/newscache/,{%_sysconfdir},/etc/rc.d/init.d/}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/newscache
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/newscache.conf-dist $RPM_BUILD_ROOT%{_sysconfdir}/newscache.conf
mv -f  $RPM_BUILD_ROOT%{_sysconfdir}/newscache.auth-dist $RPM_BUILD_ROOT%{_sysconfdir}/newscache.auth

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%doc %{_datadir}/info/NewsCache.info.gz
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
%dir %{_sysconfdir}
%attr(755,news,news) %dir	/var/cache/newscache
%attr(644,news,news) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*

%files inetd
%defattr(644,root,root,755)

%files standalone
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/newscache
%{_infodir}/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*
