Summary:	News Cache 
Summary(pl):	nisza dla newsów 
Name:		NewsCache
Version:	1.1.92
Release:	0
Epoch:		0
License:	- (enter GPL/LGPL/BSD/BSD-like/other license name here)
Group:		-
######		Unknown group!
#Vendor:		-
#Icon:		-
Source0:	http://www.hstraub.at/linux/downloads/src/%{name}-%{version}.tar.gz 
# Source0-md5:	-
#Source1:	%{name}
# Source1-md5:	-
#Patch0:		%{name}%{name}what.patch
#URL:		-
#BuildRequires:	-
#PreReq:		-
#Requires(pre,post):	-
#Requires(preun):	-
#Requires(postun):	-
#Requires:	-
#Provides:	-
#Obsoletes:	-
#Conflicts:	-
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

#%package subpackage
#Summary:	-
#Summary(pl):	-
#Group:		-
######		Unknown group!

#%description subpackage

#%description subpackage -l pl

%prep
%setup -q -n %{name}-%{version}
#%patch0 -p1

%build
# if ac/am/* rebuilding is necessary, do it in this order and add
# appropriate BuildRequires
%{__gettextize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
# create directories if necessary
#install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%pre

%post

%preun

%postun

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog NEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}

#%files subpackage
#%defattr(644,root,root,755)
#%doc extras/*.gz
#%{_datadir}/%{name}-ext
