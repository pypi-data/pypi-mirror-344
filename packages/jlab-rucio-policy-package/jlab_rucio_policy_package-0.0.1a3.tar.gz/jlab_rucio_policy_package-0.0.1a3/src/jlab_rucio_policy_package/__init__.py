SUPPORTED_VERSION = [">=37.0.0"]

def get_algorithms():
    from jlab_rucio_policy_package.lfn2pfn import lfn2pfn_jlab
    from jlab_rucio_policy_package.extract_scope import extract_scope_jlab
    return {'lfn2pfn': {'jlab': lfn2pfn_jlab},
            'scope': {'jlab': extract_scope_jlab}
           }

