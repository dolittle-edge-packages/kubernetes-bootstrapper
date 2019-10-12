Name     : kubernetes-bootstrapper
Version  : 1.0.2
Release  : 1
License  : MIT
Summary  : Dolittle Edge Kubernetes automatic bootstrapper
URL      : https://github.com/dolittle-edge-packages/kubernetes-bootstrapper
Source0  : https://github.com/dolittle-edge-packages/kubernetes-bootstrapper/archive/1.0.2.tar.gz

%description

%prep
%setup -q

%build

%install
install -D -m 644 system/60-kubernetes.conf %{buildroot}/usr/lib/sysctl.d/60-kubernetes.conf
install -D -m 644 system/90-preconfigured.conf %{buildroot}/usr/lib/systemd/system/kubelet.service.d/90-preconfigured.conf
install -D -m 644 system/99-kubernetes.conf %{buildroot}/usr/lib/systemd/system/docker.service.d/99-kubernetes.conf
install -D -m 600 system/kubernetes.nmconnection %{buildroot}/usr/lib/NetworkManager/system-connections/kubernetes.nmconnection
install -D -m 644 system/dolittle-kubernetes-certificates.service %{buildroot}/usr/lib/systemd/system/dolittle-kubernetes-certificates.service
install -D -m 644 system/dolittle-hostname-hosts.service %{buildroot}/usr/lib/systemd/system/dolittle-hostname-hosts.service
install -D -m 755 system/dolittle-add-hostnames-to-hosts %{buildroot}/usr/bin/dolittle-add-hostnames-to-hosts

mkdir -p %{buildroot}/usr/lib/systemd/system
ln -sf /dev/null %{buildroot}/usr/lib/systemd/system/dev-sda2.swap
mkdir -p %{buildroot}/usr/lib/systemd/system/multi-user.target.wants
ln -sf ../kubelet.service %{buildroot}/usr/lib/systemd/system/multi-user.target.wants/kubelet.service
ln -sf ../dolittle-kubernetes-certificates.service %{buildroot}/usr/lib/systemd/system/multi-user.target.wants/dolittle-kubernetes-certificates.service
ln -sf ../dolittle-hostname-hosts.service %{buildroot}/usr/lib/systemd/system/multi-user.target.wants/dolittle-hostname-hosts.service

install -D -m 644 manifests/etcd.yaml %{buildroot}/usr/lib/kubernetes/manifests/etcd.yaml
install -D -m 644 manifests/kube-apiserver.yaml %{buildroot}/usr/lib/kubernetes/manifests/kube-apiserver.yaml
install -D -m 644 manifests/kube-scheduler.yaml %{buildroot}/usr/lib/kubernetes/manifests/kube-scheduler.yaml
install -D -m 644 manifests/kube-proxy.yaml %{buildroot}/usr/lib/kubernetes/manifests/kube-proxy.yaml
install -D -m 644 manifests/kube-controller-manager.yaml %{buildroot}/usr/lib/kubernetes/manifests/kube-controller-manager.yaml
install -D -m 644 manifests/coredns.yaml %{buildroot}/usr/lib/kubernetes/manifests/coredns.yaml
install -D -m 644 manifests/flannel.yaml %{buildroot}/usr/lib/kubernetes/manifests/flannel.yaml

install -D -m 644 config/kubelet.yaml %{buildroot}/usr/lib/kubernetes/config/kubelet.yaml
install -D -m 644 config/kube-proxy.yaml %{buildroot}/usr/lib/kubernetes/config/kube-proxy.yaml
install -D -m 644 config/Corefile %{buildroot}/usr/lib/kubernetes/config/Corefile
install -D -m 644 config/flannel/cni-conf.json %{buildroot}/usr/lib/kubernetes/config/flannel/cni-conf.json
install -D -m 644 config/flannel/net-conf.json %{buildroot}/usr/lib/kubernetes/config/flannel/net-conf.json

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
