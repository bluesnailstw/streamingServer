%define name		DarwinStreamingServer
%define version		6.0.3
%define release		2
%define source		DarwinStreamingSrvr6.0.3-Source
%define dss_user	qtss
%define dss_group	qtss

Summary:	Apple's Darwin Streaming Server
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{source}.tar.bz2
#Source1:	dss.init.bz2
#Source2:	dss-proxy.init.bz2
#Source5:	dss.bz2
#Source6:	dss-proxy.bz2
#Patch0:	build_optimizer.patch.bz2
#Patch1:	Config.patch.bz2
#Patch2:	DEFAULTPATHS.patch.bz2
License:	Apple Public Source License
URL:		http://www.publicsource.apple.com/projects/streaming/
Group:		System/Servers
BuildRoot:	%{_tmppath}/%{name}-buildroot
Requires:	perl-Net-SSLeay
Provides:	dss dss2 dss4 dss5 DarwinStreamingServer StreamingServer
Obsoletes:	dss dss2 dss4 DarwinStreamingServer StreamingServer
Conflicts:	%{name}-Proxy

%description
Darwin Streaming Server lets you stream digital video on the
Internet using industry-standard Internet protocols RTP and RTSP.

Using Darwin Streaming Server you can serve stored files (video
on demand) or reflect live broadcasts to thousands of QuickTime
4 or later users. With its combination of industry-standard
streaming protocols and cutting-edge compression technologies,
QuickTime delivers perfectly synchronized audio and video streams
ideal for Internet video and live events.

%if %{?_with_proxy:1}%{!?_with_proxy:0}
%package	Proxy
Summary:	Apple's Darwin Streaming Proxy
Group:		System/Servers
License:	Apple Public Source License
Provides:	dss4-proxy dss-proxy %{name}-Proxy = %{version}
Obsoletes:	dss4-proxy dss-proxy %{name}-Proxy = %{version}
Conflicts:	%{name}

%description	Proxy
The Darwin Streaming Proxy is an application specific proxy which
would normally be run in a border zone or perimeter network. It
is used to give client machines within a protected network access
to streaming servers outside that network, in the case when the
firewall blocks RTSP connections or RTP/UDP data flow. The
firewall perimeter network is usually configured to allow:

* RTSP connections from within the network, as long as the
  destination is the proxy

* RTSP connections to outside the network, as long as the source
  is the proxy

* RTP datagrams to and from the proxy to the inner network

* RTP datagrams to and from the proxy to the outside
%endif

%package	Utils
Summary:	Apple's Darwin Streaming Server Movie inspection utilities
Group:		System/Servers
License:	Apple Public Source License
Provides:	dss4-utils %{name}-Utils = %{version}
Obsoletes:	dss4-utils %{name}-Utils = %{version}

%description	Utils
* QTBroadcaster
  Requires a target ip address, a source movie, one or more source
  hint track ids in movie, and an initial port. Every packet
  referenced by the hint track(s) is broadcasted to the specified
  ip address.

* QTFileInfo
  Requires a movie name. Displays each track id, name, create date,
  and mod date. If the track is a hint track, additional
  information is displayed: the total rtp bytes and packets, the
  average bit rate and packet size, and the total header
  percentage of the stream.

* QTFileTest
  Requires a movie name. Parses the Movie Header Atom and displays
  a trace of the output.

* QTRTPFileTest
  Requires a movie and a hint track id in the movie. Displays the
  RTP header (TransmitTime, Cookie, SeqNum, and TimeStamp) for
  each packet.

* QTRTPGen
  Requires a movie and a hint track id. Displays the number of
  packets in each hint track sample and writes the RTP packets to
  file "track.cache"

* QTSampleLister
  Requires a movie and a track id. Displays track media sample
  number, media time, Data offset, and sample size for each sample
  in the track.

* QTSDPGen
  Requires a list of 1 or more movies. Displays the SDP
  information for all of the hinted tracks in each movie. Use -f
  to save the SDP information to the file [movie].sdp in the same
  directory as the source movie.

* QTTrackInfo
  Requires a movie, sample table atom type, and track id. Displays
  the information in the sample table atom of the specified track.
  Supports "stco", "stsc", "stsz", "stts" as the atom type.

  Example: "./QTTrackInfo -T stco /movies/mystery.mov 3" dumps the
  chunk offset sample table in track 3.

* StreamingLoadTool

%package	Samples
Summary:	Apple's Darwin Streaming Samples
Group:		System/Servers
License:	Apple Public Source License
Provides:	dss4-samples dss-samples %{name}-Samples = %{version}
Obsoletes:	dss4-samples dss-samples %{name}-Samples = %{version}

%description	Samples
Sample files for the Darwin Streaming Server.

%prep

%setup -q -n %{source}
#%patch0 -p1
#%patch1 -p1
#%patch2 -p1

# patch streamingadminserver.pl
perl -p -i -e "s|/usr/local/|/usr/|g" WebAdmin/src/streamingadminserver.pl
perl -p -i -e "s|/etc/streaming/|/etc/dss/|g" WebAdmin/src/streamingadminserver.pl
perl -p -i -e "s|/var/streaming/logs/|/var/log/dss/|g" WebAdmin/src/streamingadminserver.pl
perl -p -i -e "s|/var/streaming/|/var/dss/|g" WebAdmin/src/streamingadminserver.pl
perl -p -i -e "s|/usr/local/|/usr/|g" WebAdmin/src/streamingadminserver.pl

# patch manpages
perl -p -i -e "s|/Library/QuickTimeStreaming/Config/|/etc/dss/|g" Documentation/man/qtss/*
perl -p -i -e "s|/Library/QuickTimeStreaming/Modules|/usr/lib/dss|g" Documentation/man/qtss/*
perl -p -i -e "s|/Library/QuickTimeStreaming/Movies|/var/dss/movies|g" Documentation/man/qtss/*
perl -p -i -e "s|/Library/QuickTimeStreaming/Playlists|/var/dss/playlists|g" Documentation/man/qtss/*
perl -p -i -e "s|/Library/QuickTimeStreaming/Logs|/var/log/dss|g" Documentation/man/qtss/*
perl -p -i -e "s|/Library/QuickTimeStreaming/Docs|%{_docdir}/%{name}-%{version}|g" Documentation/man/qtss/*
perl -p -i -e "s|QuickTimeStreamingServer|DarwinStreamingServer|g" Documentation/man/qtss/*

cat > defaultPaths.h << EOF
#define DEFAULTPATHS_DIRECTORY_SEPARATOR	"/"
#define DEFAULTPATHS_ROOT_DIR			"%{_localstatedir}/dss/"
#define DEFAULTPATHS_ETC_DIR			"%{_sysconfdir}/dss/"
#define DEFAULTPATHS_ETC_DIR_OLD		"%{_sysconfdir}/"
#define DEFAULTPATHS_SSM_DIR			"%{_libdir}/dss/"
#define DEFAULTPATHS_LOG_DIR			"%{_localstatedir}/log/dss/"
#define DEFAULTPATHS_PID_DIR			"%{_localstatedir}/run/"
#define DEFAULTPATHS_MOVIES_DIR			"%{_localstatedir}/dss/movies/"
EOF

%build
export RPM_OPT_FLAGS="%{optflags}"
export ARCH="%{_target_cpu}"
# parallel build hack... (it sucks)
# export JOBS=$(echo %{_smp_mflags}|cut -dj -f2)
# ./Buildit --jobs=$JOBS
./Buildit

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_sysconfdir}/dss
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_libdir}/dss
install -d %{buildroot}%{_localstatedir}/dss/AdminHtml
install -d %{buildroot}%{_localstatedir}/dss/AdminHtml/images
install -d %{buildroot}%{_localstatedir}/dss/AdminHtml/includes
install -d %{buildroot}%{_localstatedir}/dss/AdminHtml/html_en
install -d %{buildroot}%{_localstatedir}/dss/movies
install -d %{buildroot}%{_localstatedir}/dss/playlists
install -d %{buildroot}/var/log/dss
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_liconsdir}
install -d %{buildroot}%{_menudir}
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_mandir}/man8
#install -d %{buildroot}%{_libdir}/%{name}-Admin/scripts
install -d %{buildroot}%{_datadir}/doc/%{name}-%{version}

install -m755 DarwinStreamingServer %{buildroot}%{_sbindir}/
install -m755 PlaylistBroadcaster.tproj/PlaylistBroadcaster %{buildroot}%{_bindir}/
install -m755 MP3Broadcaster/MP3Broadcaster %{buildroot}%{_bindir}/
install -m755 qtpasswd.tproj/qtpasswd %{buildroot}%{_bindir}/
install -m755 APIModules/QTSSHomeDirectoryModule/createuserstreamingdir %{buildroot}%{_bindir}/

# NOTE! the StreamingLoadTool is not yet released as source code
install -m755 StreamingLoadTool/StreamingLoadTool %{buildroot}%{_bindir}/

# modules
install -s -m755 APIModules/QTSSHomeDirectoryModule/QTSSHomeDirectoryModule %{buildroot}%{_libdir}/dss/
install -s -m755 APIModules/QTSSRefMovieModule/QTSSRefMovieModule %{buildroot}%{_libdir}/dss/
#install -s -m755 APIModules/QTSSDemoAuthorizationModule.bproj/QTSSDemoAuthorizationModule %{buildroot}%{_libdir}/dss/
install -s -m755 APIModules/QTSSRawFileModule.bproj/QTSSRawFileModule %{buildroot}%{_libdir}/dss/
#install -s -m755 APIModules/QTSSSpamDefenseModule.bproj/QTSSSpamDefenseModule %{buildroot}%{_libdir}/dss/

# utils
install -m755 QTFileTools/QTBroadcaster.tproj/QTBroadcaster %{buildroot}%{_bindir}/
install -m755 QTFileTools/QTFileInfo.tproj/QTFileInfo %{buildroot}%{_bindir}/
install -m755 QTFileTools/QTFileTest.tproj/QTFileTest %{buildroot}%{_bindir}/
install -m755 QTFileTools/QTRTPFileTest.tproj/QTRTPFileTest %{buildroot}%{_bindir}/
install -m755 QTFileTools/QTRTPGen.tproj/QTRTPGen %{buildroot}%{_bindir}/
install -m755 QTFileTools/QTSampleLister.tproj/QTSampleLister %{buildroot}%{_bindir}/
install -m755 QTFileTools/QTSDPGen.tproj/QTSDPGen %{buildroot}%{_bindir}/
install -m755 QTFileTools/QTTrackInfo.tproj/QTTrackInfo %{buildroot}%{_bindir}/

# config
#install -m644 streamingserver.xml-POSIX %{buildroot}%{_sysconfdir}/dss/streamingserver.xml
#%{buildroot}%{_sbindir}/DarwinStreamingServer -x -c %{buildroot}%{_sysconfdir}/dss/streamingserver.xml
install -m644 streamingserver.xml-POSIX %{buildroot}%{_sysconfdir}/dss/streamingserver.xml-sample
install -m644 relayconfig.xml-Sample %{buildroot}%{_sysconfdir}/dss/relayconfig.xml
install -m644 relayconfig.xml-Sample %{buildroot}%{_sysconfdir}/dss/relayconfig.xml-sample
install -m644 qtaccess %{buildroot}%{_sysconfdir}/dss/
#install -m644 qtusers %{buildroot}%{_sysconfdir}/dss/
#install -m644 qtgroups %{buildroot}%{_sysconfdir}/dss/

# streamingadminserver
install -m755 WebAdmin/src/streamingadminserver.pl %{buildroot}%{_sbindir}/
install -m644 WebAdmin/streamingadminserver.pem %{buildroot}%{_sysconfdir}/dss/
install -m644 WebAdmin/WebAdminHtml/*.pl %{buildroot}%{_localstatedir}/dss/AdminHtml/
install -m644 WebAdmin/WebAdminHtml/*.cgi %{buildroot}%{_localstatedir}/dss/AdminHtml/
install -m644 WebAdmin/WebAdminHtml/*.html %{buildroot}%{_localstatedir}/dss/AdminHtml/
install -m644 WebAdmin/WebAdminHtml/images/*.gif %{buildroot}%{_localstatedir}/dss/AdminHtml/images/
install -m644 WebAdmin/WebAdminHtml/includes/*.js %{buildroot}%{_localstatedir}/dss/AdminHtml/includes/
install -m644 WebAdmin/WebAdminHtml/html_en/messages %{buildroot}%{_localstatedir}/dss/AdminHtml/html_en/
install -m644 WebAdmin/WebAdminHtml/html_en/genres %{buildroot}%{_localstatedir}/dss/AdminHtml/html_en/

# NOTE! the StreamingLoadTool is not yet released as source code
#install -m644 streamingloadtool.conf %{buildroot}%{_sysconfdir}/dss/streamingloadtool.conf

# doc
install -m644 Documentation/*.1 %{buildroot}%{_mandir}/man1/
install -m644 Documentation/man/qtss/*.1 %{buildroot}%{_mandir}/man1/
install -m644 Documentation/man/qtss/createuserstreamingdir.8 %{buildroot}%{_mandir}/man8/
install -m644 Documentation/man/qtss/QuickTimeStreamingServer.8 %{buildroot}%{_mandir}/man8/DarwinStreamingServer.8
install -m644 Documentation/man/qtss/streamingadminserver.pl.8 %{buildroot}%{_mandir}/man8/

# samples
install -m644 sample* %{buildroot}%{_localstatedir}/dss/movies/

# sys 5 scripts
install -m755 linux/dss.init %{buildroot}%{_initrddir}/dss

# i strongly suspect the web admin can't follow symlinks..., if
# so, some coder needs to fix the source. As the server is run
# under the dss user, there might be some problems...

ln -s %{_docdir}/%{name}-%{version} %{buildroot}%{_localstatedir}/dss/docs
ln -s %{_sysconfdir}/dss %{buildroot}%{_localstatedir}/dss/config
ln -s /usr/lib/dss %{buildroot}%{_localstatedir}/dss/modules
ln -s ../log/dss %{buildroot}%{_localstatedir}/dss/logs

# provide ghost logs...
touch %{buildroot}/var/log/dss/Error.log
touch %{buildroot}/var/log/dss/StreamingServer.log
touch %{buildroot}/var/log/dss/mp3_access.log
touch %{buildroot}/var/log/dss/server_status

# Proxy files
%if %{?_with_proxy:1}%{!?_with_proxy:0}
install -m755 StreamingProxy.tproj/StreamingProxy %{buildroot}%{_sbindir}/
install -m644 StreamingProxy.tproj/streamingproxy.conf %{buildroot}%{_sysconfdir}/dss/
install -m644 StreamingProxy.tproj/streamingproxy.conf %{buildroot}%{_sysconfdir}/dss/streamingproxy.conf.default
install -m755 linux/dss-proxy.init %{buildroot}%{_initrddir}/dss-proxy

touch %{buildroot}/var/log/dss/StreamingProxy.log
%endif

%pre
# Shut down a previously installed server first
if test -x %{_sysconfdir}/init.d/dss
then
  %{_sysconfdir}/init.d/dss stop
  sleep 5
elif test -x %{_sysconfdir}/rc.d/init.d/dss
then
  %{_sysconfdir}/rc.d/init.d/dss stop
  sleep 5
fi

# Create a dss user and group. Do not report any problems if it already
# exists.
groupadd -r %{dss_group} 2> /dev/null || true
useradd -M -r -d %{_localstatedir}/dss -s /bin/bash -c "Darwin Streaming Server" -g %{dss_group} %{dss_user} 2> /dev/null || true 
# The user may already exist, make sure it has the proper group nevertheless
usermod -g %{dss_group} %{dss_user} 2> /dev/null || true

%post
# Create qtusers and qtgroups if they don't already exsist
if [ ! -e %{_sysconfdir}/dss/qtusers ]; then
	echo "Creating administrator user with default password "password". Please change it by running qtpasswd"
	%{_bindir}/qtpasswd -c -p password administrator >/dev/null 2>&1
	
	# Add the new admin username to /etc/streaming/qtgroups
	# and delete the default admin username
	echo "admin: administrator" >%{_sysconfdir}/dss/qtgroups
fi

# Make Darwin create the config file
if [ ! -e %{_sysconfdir}/dss/streamingserver.xml ]; then
	%{_sbindir}/DarwinStreamingServer -x  >/dev/null 2>&1
	chmod 600 %{_sysconfdir}/dss/streamingserver.xml
	chown %{dss_user} %{_sysconfdir}/dss/streamingserver.xml
else
	echo "warning: %{_sysconfdir}/dss/streamingserver.xml created as %{_sysconfdir}/dss/streamingserver.xml.rpmnew"
	%{_sbindir}/DarwinStreamingServer -x -c %{_sysconfdir}/dss/streamingserver.xml.rpmnew >/dev/null 2>&1
	chmod 600 %{_sysconfdir}/dss/streamingserver.xml.rpmnew
	chown %{dss_user} %{_sysconfdir}/dss/streamingserver.xml.rpmnew
fi

# Make dss start/shutdown automatically when the machine does it.
# use insserv for older SuSE Linux versions
if test -x /sbin/insserv
then
	/sbin/insserv %{_sysconfdir}/init.d/dss
# use chkconfig on Red Hat and newer SuSE releases
elif test -x /sbin/chkconfig
then
	/sbin/chkconfig --add dss
fi

chown -R %{dss_user}.%{dss_group} %{_sysconfdir}/dss
chown -R %{dss_user}.%{dss_group} %{_localstatedir}/dss

if test -x %{_sysconfdir}/init.d/dss
then
  %{_sysconfdir}/init.d/dss start
elif test -x %{_sysconfdir}/rc.d/init.d/dss
then
  %{_sysconfdir}/rc.d/init.d/dss start
fi

%preun
# Shut down server before uninstalling it
if test -x %{_sysconfdir}/init.d/dss
then
  %{_sysconfdir}/init.d/dss stop > /dev/null 2>&1
  sleep 5
elif test -x %{_sysconfdir}/rc.d/init.d/dss
then
  %{_sysconfdir}/rc.d/init.d/dss stop > /dev/null 2>&1
  sleep 5
fi

# Remove autostart
# for older SuSE Linux versions
if test -x /sbin/insserv
then
	/sbin/insserv -r %{_sysconfdir}/init.d/dss
# use chkconfig on Red Hat and newer SuSE releases
elif test -x /sbin/chkconfig
then
	/sbin/chkconfig --del dss
fi

%postun
#%_postun_userdel dss

%if %{?_with_proxy:1}%{!?_with_proxy:0}
%post Proxy
if test -x %{_sysconfdir}/init.d/dss-proxy
then
  %{_sysconfdir}/init.d/dss-proxy start
  sleep 5
elif test -x %{_sysconfdir}/rc.d/init.d/dss-proxy
then
  %{_sysconfdir}/rc.d/init.d/dss-proxy start
  sleep 5
fi

%preun Proxy
if test -x %{_sysconfdir}/init.d/dss-proxy
then
  %{_sysconfdir}/init.d/dss-proxy stop > /dev/null 2>&1
  sleep 5
elif test -x %{_sysconfdir}/rc.d/init.d/dss-proxy
then
  %{_sysconfdir}/rc.d/init.d/dss-proxy stop > /dev/null 2>&1
  sleep 5
fi
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc APPLE_LICENSE ReleaseNotes.txt
#%doc APIModules/QTSSRawFileModule.bproj/README-RawFileModule
#%doc APIModules/QTSSRawFileModule.bproj/sampleredirect.raw
%doc Documentation/3rdPartyAcknowledgements.rtf
#%doc Documentation/AboutDarwinStreamingSvr.pdf
%doc Documentation/AboutQTFileTools.html
%doc Documentation/AboutTheSource.html
%doc Documentation/admin-protocol-README.txt
%doc Documentation/CachingProxyProtocol-README.txt
%doc Documentation/DevNotes.html
%doc Documentation/draft-serenyi-avt-rtp-meta-00.txt
%doc Documentation/DSS_QT_Logo_License.pdf
%doc Documentation/License.rtf
%doc Documentation/QTSSAPIDocs.pdf
%doc Documentation/ReadMe.rtf
%doc Documentation/readme.txt
%doc Documentation/ReliableRTP_WhitePaper.rtf
%doc Documentation/RTSP_Over_HTTP.pdf
%config(noreplace) %attr(0755, root, root) %{_initrddir}/dss
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/dss/qtaccess
#%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/dss/qtgroups
#%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/dss/qtusers
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/dss/relayconfig.xml
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/dss/relayconfig.xml-sample
#%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/dss/streamingserver.xml
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/dss/streamingserver.xml-sample
%dir %attr(0755, root, root) %{_bindir}/MP3Broadcaster
%dir %attr(0755, root, root) %{_bindir}/PlaylistBroadcaster
%dir %attr(0755, root, root) %{_bindir}/qtpasswd
%dir %attr(0755, root, root) %{_bindir}/createuserstreamingdir
%dir %attr(0755, root, root) %{_sbindir}/DarwinStreamingServer
%dir %attr(0755, root, root) %{_sbindir}/streamingadminserver.pl
%dir %attr(0755, root, root) %{_sysconfdir}/dss/streamingadminserver.pem
%dir %attr(0755, root, root) %{_libdir}/dss
#%attr(0755, root, root) %{_libdir}/dss/QTSSDemoAuthorizationModule
%attr(0755, root, root) %{_libdir}/dss/QTSSRawFileModule
#%attr(0755, root, root) %{_libdir}/dss/QTSSSpamDefenseModule
%attr(0755, root, root) %{_libdir}/dss/QTSSRefMovieModule
%attr(0755, root, root) %{_libdir}/dss/QTSSHomeDirectoryModule
%dir %attr(0775, %{dss_user}, %{dss_group}) %{_localstatedir}/dss/movies
%dir %attr(0755, %{dss_user}, %{dss_group}) %{_localstatedir}/dss/playlists
%dir %attr(0755, root, root) %{_localstatedir}/dss/docs
%dir %attr(0755, root, root) %{_localstatedir}/dss/config
%dir %attr(0755, root, root) %{_localstatedir}/dss/modules
%dir %attr(0755, %{dss_user}, %{dss_group}) %{_localstatedir}/dss/logs
%dir %attr(0755, root, root) %{_localstatedir}/dss/AdminHtml/*
%dir %attr(0755, root, root) %{_localstatedir}/dss/AdminHtml/html_en/*
%dir %attr(0755, root, root) %{_localstatedir}/dss/AdminHtml/images/*
%dir %attr(0755, root, root) %{_localstatedir}/dss/AdminHtml/includes/*
%dir %attr(0755, %{dss_user}, %{dss_group}) %{_localstatedir}/log/dss
%attr(644,%{dss_user},%{dss_group}) %verify(not md5 size mtime) %ghost /var/log/dss/Error.log
%attr(644,%{dss_user},%{dss_group}) %verify(not md5 size mtime) %ghost /var/log/dss/StreamingServer.log
%attr(644,%{dss_user},%{dss_group}) %verify(not md5 size mtime) %ghost /var/log/dss/mp3_access.log
%attr(644,%{dss_user},%{dss_group}) %verify(not md5 size mtime) %ghost /var/log/dss/server_status
%attr(0644, root, root) %{_mandir}/man1/*
%attr(0644, root, root) %{_mandir}/man8/*

%if %{?_with_proxy:1}%{!?_with_proxy:0}
%files Proxy
%defattr(-, root, root)
%doc APPLE_LICENSE Documentation/CachingProxyProtocol-README.txt
%doc StreamingProxy.tproj/StreamingProxy.html
%config(noreplace) %attr(0755, root, root) %{_initrddir}/dss-proxy
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/dss/streamingproxy.conf
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/dss/streamingproxy.conf.default

%dir %attr(0755, root, root) %{_sbindir}/StreamingProxy
%dir %attr(0755, root, root) %{_localstatedir}/dss/config
%dir %attr(0755, %{dss_user}, %{dss_group}) %{_localstatedir}/dss/logs
%dir %attr(0755, %{dss_user}, %{dss_group}) %{_localstatedir}/log/dss
%attr(644,root,root) %verify(not md5 size mtime) %ghost /var/log/dss/StreamingProxy.log
%endif

%files Utils
%defattr(-, root, root)
%doc APPLE_LICENSE Documentation/AboutQTFileTools.html
%dir %attr(0755, root, root) %{_bindir}/QTBroadcaster
%dir %attr(0755, root, root) %{_bindir}/QTFileInfo
%dir %attr(0755, root, root) %{_bindir}/QTFileTest
%dir %attr(0755, root, root) %{_bindir}/QTRTPFileTest
%dir %attr(0755, root, root) %{_bindir}/QTRTPGen
%dir %attr(0755, root, root) %{_bindir}/QTSampleLister
%dir %attr(0755, root, root) %{_bindir}/QTSDPGen
%dir %attr(0755, root, root) %{_bindir}/QTTrackInfo
%dir %attr(0755, root, root) %{_bindir}/StreamingLoadTool

%files Samples
%defattr(-, root, root)
%dir %attr(0664, %{dss_user}, %{dss_group}) %{_localstatedir}/dss/movies/sample*

%changelog
* Sat May 31 2008 Sverker Abrahamsson <sverker@abrahamsson.com> 6.0.3-2
- Support for x86_64

* Sat May 24 2008 Sverker Abrahamsson <sverker@abrahamsson.com> 6.0.3-1
- Adapted for Darwin 6.0.3

* Fri Oct 1 2004 Sverker Abrahamsson <sverker@abrahamsson.com> 5.5.5
- Adapted for Fedora and newer version of package

* Fri Jul 11 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.1.3-2mdk
- rebuild

* Mon Jun 16 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.1.3-1mdk
- 4.1.3

* Thu Jan 16 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.1.1-3mdk
- build release

* Fri Nov 22 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.1.1-2mdk
- since i never got the %{name}-Admin package to really work, and 
  no one ever helped me fixing it, drop it. it's no loss, it's garbage 
  anyway. also drop the %{name}-Media package (waste of bandwidth when
  mirroring)
- also drop S3, S4, S7, S8, S9, S10 and P3 (not needed anymore)

* Sat Nov 09 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.1.1-1mdk
- new version
- make Mr. Lint happier...
- fix locations in the patches (%{_localstatedir}/dss)

* Mon Aug 19 2002 Laurent Culioli <laurent@pschit.net> 4.1-3mdk
- Rebuild with gcc3.2

* Sun Aug  4 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.1-2mdk
- rebuilt with gcc-3.2

* Tue Jul 23 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.1-1mdk
- final version! (4.1)
- rediffed all patches
- misc spec file fixes
- the web admin gui still does not work..., a perl wizard really
  needs to look into this _please_

* Sat Jun 29 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.1-0.20020629.1mdk
- new CVS version

* Fri Jun 14 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.1-0.20020614.1mdk
- new CVS version

* Sun Jun 02 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 4.1-0.20020601.2mdk
- png icons for menu (out xpm!)

* Sat Jun  1 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.1-0.20020601.1mdk
- new CVS version (build 423)

* Wed May 29 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.1-0.20020529.1mdk
- new CVS version
- some spec file cleanups

* Thu May  6 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.1-0.20020506.1mdk
- new CVS version
- the source rpm for 4.1-0.20020502.1mdk was lost in cyberspace

* Thu May  2 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.1-0.20020502.1mdk
- new CVS version (thread safe std lib calls support)
- rediffs
- included the new "RefMovieModule"

* Tue Apr 27 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.1-0.20020427.1mdk
- new CVS version (build 419)
- included a new pid file dir in defaultPaths.h
- included a new dynamic tag (versioning) hack

* Tue Apr 24 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.1-0.20020424.1mdk
- new CVS version (did not compile)

* Tue Apr 16 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.1-0.20020416.1mdk
- new CVS version (build 418) (did not compile)

* Tue Apr 16 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.1-0.20020415.3mdk
- bzip all sources
- fix the menu stuff...

* Tue Apr 16 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.1-0.20020415.2mdk
- fixed status in the Admin init script (S3), fixed the "right" permissions in
  /etc/dss/* when running the dss-admin_setup.sh script. These fixes were sent by
  Andre Duclos <Andre.Duclos@cnes.fr>, Thanks man!
- provide ghost logs, also fix logrotate for the new realtime server_status
  feature.
- provide a simple X menu entry and icons for the Admin stuff

* Mon Apr 15 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.1-0.20020415.1mdk
- new CVS version (build 417)
- fixed the "right" permissions in /etc/dss/* (again?)
 
* Tue Apr  9 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.1-0.20020409.1mdk
- I was using the wrong numbering scheme, pointed out by Frédéric Crozat.

* Tue Apr  9 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.0.20020409-2mdk
- fix references for streamingadminserver to StreamingAdminServer (!)
  now you can stop it too :-)

* Tue Apr  9 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.0.20020409-1mdk
- new CVS version
- I think I've found why the web gui wasn't working...
- more default values added to the xml conf files.
- spec file fixes

* Mon Apr  8 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.0.20020408-1mdk
- the previous update was lost in cyber space...
- init script fixes
- new CVS version
- rediffs
- spec file fixes

* Wed Mar 20 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.0.20020320-6mdk
- useradd suddenly stopped workin (!) - fixed now...

* Tue Mar 19 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.0.20020319-5mdk
- Mr. rpmlint fixes
- the proxy server does not like tabs in the config (!)
- remade the sys5 scripts

* Tue Mar 19 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.0.20020319-4mdk
- (who's counting...)
- added P2 & P3 inspired by Peter Brays patches
- broke out the sample movies into a sub package
- removed the sample mp3 file

* Mon Mar 18 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.0-3mdk
- third attempt with a better P0 & P1...

* Sun Mar 17 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.0-2mdk
- second attempt with a fresh CVS version...

* Sat Mar 16 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.0-1mdk
- first attempt at this beast...
- added S1 - S7, P0 - P1

