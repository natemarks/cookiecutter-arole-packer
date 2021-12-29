import os
import testinfra.utils.ansible_runner

testinfra_hosts =  testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_version_file(host):
    ''' Check the default version file 
    sdg
    dfg
    '''
    f = host.file('/tmp/version.txt')
    
    assert f.exists
    assert f.mode == 0o644