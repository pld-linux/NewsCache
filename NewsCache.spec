# TODO:	review i and tests (especially .inet), %%post, %%preun,
#	%%postun scripts for NewsCache-{standalone,inet}, fix 
#	subpackages group descriptions.
#
Summary:	News Cache
Summary(pl):	nisza dla newsów
Name:		NewsCache
Version:	1.1.92
Release:	1
Epoch:		0
License:	GPL
Group:		Applications/News
Source0:	http://www.hstraub.at/linux/downloads/src/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.inet
# Source0-md5:	8cd84c15429fbf70b9f24ab877387ab3
Patch0:		%{name}-ac_no_debug_flag_hack.patch
# http://cmeerw.org/debian/
# http://download.cmeerw.net/debian/newscache/source/newscache_1.1.92-0cmeerw.diff.gz
Patch1:		http://download.cmeerw.net/debian/newscache/source/newscache_1.1.92-0cmeerw.diff.gz
URL:		http://members.aon.at/hstraub/linux/newscache
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	socket++-devel
BuildRequires:	libwrap-devel
#Requires(pre):	/bin/id
#Requires(pre):	/usr/bin/getgid
#Requires(pre):	/usr/sbin/groupadd
#Requires(pre):	/usr/sbin/useradd
#Requires(postun):	/usr/sbin/userdel
#Requires(postun):	/usr/sbin/groupdel
#Requires(post,preun):	/sbin/chkconfig
#Requires(post,postun):	/sbin/ldconfig
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
Obsoletes:	%{name}-inetd

%description standalone
Run NewsCache in the standalone mode.

%description standalone -l pl
Uruchamia NewsCache w trybie samodzielnym.

%package inetd
Summary:	NewsCache inetd mode
Summary(pl):	NewsCache w trybie inetd
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	rc-inetd
Obsoletes:	%{name}-standalone

%description inetd
Run NewsCache from the inetd.

%description inetd -l pl
Uruchamia NewsCache pod konrol± inetd.

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
install -d $RPM_BUILD_ROOT{/var/cache/newscache,{%_sysconfdir},/etc/{rc.d/init.d,sysconfig/rc-inetd}}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/newscache
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/newscache
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/newscache.conf-dist $RPM_BUILD_ROOT%{_sysconfdir}/newscache.conf
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/newscache.auth-dist $RPM_BUILD_ROOT%{_sysconfdir}/newscache.auth

%clean
rm -rf $RPM_BUILD_ROOT

# setup provides this user/group
#%%pre
#if [ "`getgid news`" ]; then
#	/usr/sbin/groupadd -g 13 -r -f news
#fi
#if [ "`id -u news 2>/dev/null`" ]; then
#	/usr/sbin/useradd -u 9 -r -d /var/spool/news -s /bin/false -c "NEWS User" -g news news 1>&2
#fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%doc %{_infodir}/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
%config(noreplace) %verify(not size mtime md5) %attr(755,news,news) %dir /var/cache/newscache
%dir %{_sysconfdir}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*

%files inetd
%defattr(644,root,root,755)
%attr(640,root,root) /etc/sysconfig/rc-inetd/newscache

%files standalone
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/newscache
