%define oname livestreamer

Name:           python3-%{oname}
Version:        1.12.2
Release:        1
License:        BSD and MIT
Summary:        Extracts streams and pipes them into a video player of choice
Url:            http://livestreamer.tanuki.se/
Group:          Sound
Source:         https://pypi.python.org/packages/source/l/%{oname}/%{oname}-%{version}.tar.gz
BuildRequires:  pkgconfig(python)
BuildRequires:  python-setuptools
BuildRequires:  python-requests
#BuildRequires:  python-sphinx
BuildRequires:  python-singledispatch
BuildRequires:  python-urllib3
BuildRequires: dos2unix
Conflicts:  python-%{oname}
BuildArch:      noarch

%description
Livestreamer is a CLI program that extracts streams from various services and
pipes them into a video player of choice.
Livestreamer is built upon a plugin system which allows support for new
services to be easily added.

%files
%doc *.rst LICENSE* 
%{_docdir}/%{oname}/html/
%{_bindir}/%{oname}
%{py3_puresitedir}/%{oname}
%{py3_puresitedir}/%{oname}_cli
%{py3_puresitedir}/%{oname}-%{version}-py*.egg-info
%{_mandir}/man1/%{oname}.1.*
#-------------------------------------------------------------------------------------

%prep
%setup -qn %{oname}-%{version}

# edit .py file and use python3
find . -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'

# delete version-control-internal-file
find . -name .gitignore -exec rm -f {} \; >/dev/null
# Remove bundled egg-info
rm -rf src/livestreamer.egg-info

%build
%{__python3} setup.py build

# Generate man page and html documentation (needs python-sphinx)
#{__python3} setup.py build_sphinx -b man
#{__python3} setup.py build_sphinx -b html

pushd build/lib/livestreamer/packages/flashmedia
find . -type f -name "*.py" -exec chmod +x {} \;
popd

%install
%{__python3} setup.py install --root=%{buildroot} --skip-build

# install man page
install -p -d -m755 %{buildroot}%{_mandir}/man1
#install -p -m644 build/sphinx/man/%{oname}.1 %buildroot%{_mandir}/man1/%{oname}.1

# install html docs
install -p -d -m755 %{buildroot}%{_docdir}/%{oname}
mv build/sphinx/html %{buildroot}%{_docdir}/%{oname} 

# convert to unix format due rpmlint warning W: wrong-file-end-of-line-encoding
dos2unix %{buildroot}%{_docdir}/%{oname}/html/_static/jquery.js

# convert to utf8 due rpmling warning W: file-not-utf8 /usr/share/doc/python-livestreamer/html/objects.inv
iconv -f iso-8859-1 -t utf-8 %{buildroot}%{_docdir}/%{oname}/html/objects.inv > objects.inv.utf8; \
mv objects.inv.utf8 %{buildroot}%{_docdir}/%{oname}/html/objects.inv

# convert to unix format due rpmlint warning W: wrong-file-end-of-line-encoding
dos2unix %{buildroot}%{_docdir}/%{oname}/html/objects.inv

# Sphinx info file for hashing, no longer needed 
#rm %{buildroot}%{_docdir}/%{oname}/html/.buildinfo
pushd %{buildroot}%{py3_puresitedir}/%{oname}/packages/flashmedia
chmod -x {types,box,amf,compat,ordereddict}.py
popd
chmod +x %{buildroot}%{py3_puresitedir}/%{oname}/plugins/tvplayer.py
chmod +x %{buildroot}%{py3_puresitedir}/%{oname}/plugins/tv3cat.py

%check
%{__python3} setup.py test


