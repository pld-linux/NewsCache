Summary:	News Cache 
Summary(pl):	nisza dla newsów 
Name:		NewsCache
Version:	1.1.92
Release:	1
Epoch:		0
License:	GPL
Group:		Applications/News
Source0:	http://www.hstraub.at/linux/downloads/src/%{name}-%{version}.tar.gz 
# Source0-md5:	8cd84c15429fbf70b9f24ab877387ab3
Patch0:		%{name}-ac_no_debug_flag_hack.patch
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
NewsCache to wolnodostêpny serwer keszuj±cy dla sieci USENET. NewsCache
jest widziany jako serwer nntp, ale przechowuje tylko te artyku³y o które choæ jeden klient poprosi³.
NewsCache rozwi±zuje problemy takie jak zajmowanie pasma czy obci±¿enie IO... (NYF!!!)

%prep
%setup -q 
%patch0 -p0

%build
%define specflags '-O0'
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
%{_sysconfdir}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*
