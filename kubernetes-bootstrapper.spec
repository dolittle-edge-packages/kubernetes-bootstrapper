Name     : kubernetes-bootstrapper
Version  : 1.0.0
Release  : 1
License  : MIT
Summary  : Dolittle Edge Kubernetes automatic bootstrapper
URL      : https://github.com/dolittle-edge-packages/kubernetes-bootstrapper
Source0  : file://system/60-kubernetes.conf
Source1  : file://system/90-preconfigured.conf
Source2  : file://system/99-kubernetes.conf
Source3  : file://system/kubernetes.nmconnection
Source4  : file://system/dolittle-kubernetes-certificates.service
Source5  : file://system/dolittle-hostname-hosts.service
Source6  : file://system/dolittle-add-hostnames-to-hosts
Source7  : file://manifests/etcd.yaml
Source8  : file://manifests/kube-apiserver.yaml
Source9  : file://manifests/kube-scheduler.yaml
Source10 : file://manifests/kube-proxy.yaml
Source11 : file://manifests/kube-controller-manager.yaml
Source12 : file://manifests/coredns.yaml
Source13 : file://manifests/flannel.yaml
Source14 : file://config/kubelet.yaml
Source15 : file://config/kube-proxy.yaml
Source16 : file://config/Corefile.yaml
Source17 : file://config/flannel/cni-conf.json
Source18 : file://config/flannel/net-conf.json

%description

%prep

%build

%install
ln -sf /dev/null %{buildroot}/usr/lib/systemd/system/dev-sda2.swap
install -D -m 644 %{SOURCE0} %{buildroot}/usr/lib/sysctl.d/60-kubernetes.conf
install -D -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/kubelet.service.d/90-preconfigured.conf
install -D -m 644 %{SOURCE2} %{buildroot}/usr/lib/systemd/system/docker.service.d/99-kubernetes.conf
install -D -m 600 %{SOURCE3} %{buildroot}/usr/lib/NetworkManager/system-connections/kubernetes.nmconnection
install -D -m 644 %{SOURCE4} %{buildroot}/usr/lib/systemd/system/dolittle-kubernetes-certificates.service
ln -sf ../dolittle-kubernetes-certificates.service %{buildroot}/usr/lib/systemd/system/multi-user.target.wants/dolittle-kubernetes-certificates.service
install -D -m 644 %{SOURCE5} %{buildroot}/usr/lib/systemd/system/dolittle-hostname-hosts.service
ln -sf ../dolittle-hostname-hosts.service %{buildroot}/usr/lib/systemd/system/multi-user.target.wants/dolittle-hostname-hosts.service
install -D -m 755 %{SOURCE6} %{buildroot}/usr/bin/dolittle-add-hostnames-to-hosts
ln -sf ../kubelet.service %{buildroot}/usr/lib/systemd/system/multi-user.target.wants/kubelet.service

install -D -m 644 %{SOURCE7} %{buildroot}/usr/lib/kubernetes/manifests/etcd.yaml
install -D -m 644 %{SOURCE8} %{buildroot}/usr/lib/kubernetes/manifests/kube-apiserver.yaml
install -D -m 644 %{SOURCE9} %{buildroot}/usr/lib/kubernetes/manifests/kube-scheduler.yaml
install -D -m 644 %{SOURCE10} %{buildroot}/usr/lib/kubernetes/manifests/kube-proxy.yaml
install -D -m 644 %{SOURCE11} %{buildroot}/usr/lib/kubernetes/manifests/kube-controller-manager.yaml
install -D -m 644 %{SOURCE12} %{buildroot}/usr/lib/kubernetes/manifests/coredns.yaml
install -D -m 644 %{SOURCE13} %{buildroot}/usr/lib/kubernetes/manifests/flannel.yaml

install -D -m 644 %{SOURCE14} %{buildroot}/usr/lib/kubernetes/config/kubelet.yaml
install -D -m 644 %{SOURCE15} %{buildroot}/usr/lib/kubernetes/config/kube-proxy.yaml
install -D -m 644 %{SOURCE16} %{buildroot}/usr/lib/kubernetes/config/Corefile
install -D -m 644 %{SOURCE17} %{buildroot}/usr/lib/kubernetes/config/flannel/cni-conf.json
install -D -m 644 %{SOURCE18} %{buildroot}/usr/lib/kubernetes/config/flannel/net-conf.json

%post
%systemd_post dolittle-kubernetes-certificates.service
%systemd_post dolittle-hostname-hosts.service

%preun
%systemd_preun dolittle-kubernetes-certificates.service
%systemd_preun dolittle-hostname-hosts.service

%postun
%systemd_postun_with_restart dolittle-kubernetes-certificates.service
%systemd_postun_with_restart dolittle-hostname-hosts.service

%files
%defattr(-, root, root, -)

# bins
/usr/bin/dolittle-add-hostnames-to-hosts

# manifests
/usr/lib/kubernetes/manifests/etcd.yaml
/usr/lib/kubernetes/manifests/kube-apiserver.yaml
/usr/lib/kubernetes/manifests/kube-scheduler.yaml
/usr/lib/kubernetes/manifests/kube-proxy.yaml
/usr/lib/kubernetes/manifests/kube-controller-manager.yaml
/usr/lib/kubernetes/manifests/coredns.yaml
/usr/lib/kubernetes/manifests/flannel.yaml

# conf
/usr/lib/sysctl.d/60-kubernetes.conf
/usr/lib/systemd/system/kubelet.service.d/90-preconfigured.conf
/usr/lib/systemd/system/docker.service.d/99-kubernetes.conf
/usr/lib/NetworkManager/system-connections/kubernetes.nmconnection
/usr/lib/kubernetes/config/kubelet.yaml
/usr/lib/kubernetes/config/kube-proxy.yaml
/usr/lib/kubernetes/config/Corefile
/usr/lib/kubernetes/config/flannel/cni-conf.json
/usr/lib/kubernetes/config/flannel/net-conf.json

# services
/usr/lib/systemd/system/dev-sda2.swap
/usr/lib/systemd/system/dolittle-kubernetes-certificates.service
/usr/lib/systemd/system/multi-user.target.wants/dolittle-kubernetes-certificates.service
/usr/lib/systemd/system/dolittle-hostname-hosts.service
/usr/lib/systemd/system/multi-user.target.wants/dolittle-hostname-hosts.service
/usr/lib/systemd/system/multi-user.target.wants/kubelet.service

%changelog
