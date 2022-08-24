Name:          rocksdb
Version:       6.8.1
Release:       4
Summary:       A Persistent Key-Value Store for Flash and RAM Storage
 
License:       GPLv2 and Apache 2.0 License
URL:           https://github.com/facebook/rocksdb.git
 
BuildRequires: gcc make rpm-build gcc-c++ gtest-devel maven java-1.8.0-openjdk-devel

# enable debuginfo pacakges by default, then we need gdb package
BuildRequires: gdb

# rocksdb recommend installing some compression libraries
BuildRequires: snappy snappy-devel zlib zlib-devel bzip2 bzip2-devel lz4 lz4-devel zstd zstd-devel gflags gflags-devel

Requires:      snappy snappy-devel zlib zlib-devel bzip2 bzip2-devel lz4 lz4-devel zstd zstd-devel gflags gflags-devel
 
Source0:       https://codeload.github.com/facebook/%{name}/tar.gz/v%{version}
Source1:       https://repo1.maven.org/maven2/org/assertj/assertj-core/1.7.1/assertj-core-1.7.1.jar
Source2:       https://repo1.maven.org/maven2/cglib/cglib/2.2.2/cglib-2.2.2.jar
Source3:       https://repo1.maven.org/maven2/org/mockito/mockito-all/1.10.19/mockito-all-1.10.19.jar
Patch0:        rocksdb-6.8.1-install_path.patch
Patch1:        some-jar-packs-should-provides-local.patch
 
%description
Rocksdb is a library that forms the core building block for a fast key value
server, especially suited for storing data on flash drives. It has a
Log-Structured-Merge-Database (LSM) design with flexible trade offs between
Write-Amplification-Factor (WAF), Read-Amplification-Factor (RAF) and
Space-Amplification-Factor (SAF). It has multithreaded compaction, making it
specially suitable for storing multiple terabytes of data in a single database.

%package devel
Summary:       Development files for rocksdb
Requires:      %{name}%{?_isa} = %{version}-%{release}
 
%description devel
Development files for rocksdb
 
%package -n %{name}jni
Summary:       A Java JNI driver to rocksdb
# rocksdbjni.jar contains a shared object, that requires some packages
Requires:      java-1.8.0-openjdk glibc snappy zlib bzip2 lz4 zstd libstdc++ 

%description -n %{name}jni
RocksDB JNI gives you a Java interface to the RocksDB C++ library which is an
embeddable persistent key-value store for fast storage.

%prep
%autosetup -p1

rm -rf third-party/gtest-1.8.1
rm java/benchmark/src/main/java/org/rocksdb/benchmark/DbBenchmark.java
rm build_tools/gnu_parallel
mkdir -p java/test-libs
cp -p %{SOURCE1} %{SOURCE2} %{SOURCE3} java/test-libs
 
%build
export CFLAGS="%{optflags}"
# librocksdb*.so* has undefined symbols dlopen and so on, “-ldl” needs to be added here
export EXTRA_CXXFLAGS=" -std=c++11 %{optflags} -ldl"
%make_build shared_lib
# build rocksdbjni
export JAVA_HOME=%{_jvmdir}/java-1.8.0-openjdk
export EXTRA_CXXFLAGS="${EXTRA_CXXFLAGS} -I${JAVA_HOME}/include/ -I${JAVA_HOME}/include/linux"
sed -i 's#\(^DEBUG_LEVEL.*=\).*$#\10#' Makefile
sed -i '2057 a\	$(AM_V_at)cd java/target;strip $(ROCKSDBJNILIB)'  Makefile
PORTABLE=1 %make_build rocksdbjava
 
%install
make install-shared \
         INSTALL_PREFIX=%{buildroot}\
         LIB_INSTALL_DIR=%{_libdir}\
         INCLUDE_INSTALL_DIR=%{_includedir}

# install rocksdbjni
install -d -p -m 0755 %{buildroot}%{_javadir}/%{name}jni
install -D -m 0644 java/target/%{name}jni-%{version}-linux$(getconf LONG_BIT).jar \
    %{buildroot}%{_javadir}/%{name}jni/%{name}jni.jar

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
 
 
%files
%{_libdir}/librocksdb.so.6
%{_libdir}/librocksdb.so.6.8
%{_libdir}/librocksdb.so.6.8.1
%license COPYING LICENSE.Apache LICENSE.leveldb

 
%files devel
%{_libdir}/librocksdb.so
%{_includedir}/*
 
%files -n %{name}jni
%dir %{_javadir}/%{name}jni
%{_javadir}/%{name}jni/%{name}jni.jar

%changelog
* Tue Aug 23 2022 wulei <wulei80@h-partners.com> - 6.8.1-4
- Fix binary not striped problem

* Thu 01 Jul 2021 sunguoshuai <sunguoshuai@huawei.com> - 6.8.1-3
- Some jar packs should provides local in case of build error

* Thu May 06 2021 herengui <herengui@uniontech.com> - 6.8.1-2
- add java-api: rocksdbjni
- fix undefined symbol issue for c++ API

* Thu May 28 2020 openEuler Buildteam <buildteam@openeuler.org> - 6.8.1-1
- Package init
