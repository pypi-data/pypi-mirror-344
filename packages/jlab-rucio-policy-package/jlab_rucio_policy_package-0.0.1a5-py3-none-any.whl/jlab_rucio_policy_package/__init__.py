SUPPORTED_VERSION = [">=37.0.0"]

def get_algorithms():
    from jlab_rucio_policy_package.lfn2pfn import JlabRSEDeterministicTranslation
    from jlab_rucio_policy_package.extract_scope import JlabScopeExtractionAlgorithm
    return {'lfn2pfn': {'jlab': JlabRSEDeterministicTranslation.lfn2pfn_jlab},
            'scope': {'jlab': JlabScopeExtractionAlgorithm.extract_scope_jlab}
           }

