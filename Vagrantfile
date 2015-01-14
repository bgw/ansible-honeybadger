# THIS SCRIPT IS IN-PROGRESS. Don't try to use it yet.

script = <<SCRIPT
rm -rf hosts host_vars group_vars
./autosetup
SCRIPT

Vagrant.configure("2") do |config|
    config.vm.hostname = "honeybadger.local"
    # the 172.16 address space isn't commonly used
    config.vm.network "private_network", ip: "172.16.200.3"

    config.vm.box = "ubuntu/trusty32"

    config.vm.provision :ansible do |ansible|
        ansible.playbook = "site.yml"
        ansible.host_key_checking = false
        ansible.extra_vars = {testing: true}
        ansible.verbose = "vvvv"
    end

    def set_memory(vm, memory)
        vm.provider :virtualbox do |virtualbox|
            virtualbox.memory = memory
        end

        vm.provider :vmware_fusion do |vmware|
            vmware.vmx["memsize"] = memory.to_s
        end
    end

    if Vagrant.has_plugin? "vagrant-cachier"
        config.cache.enable :apt
        config.cache.scope = :box
    end

    config.vm.define "full", primary: true do |full|
        full
    end
end
