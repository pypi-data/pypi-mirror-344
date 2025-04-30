# JlabRucio policy package

This is a prototype of the Rucio policy package for Jlab



## Source files

The package currently contains the following files :
* `__init__.py` - registers the SURL, SCOPE and LFN2PFN algorithms when the package is loaded.
* `lfn2pfn.py` - contains the Jlab lfn2pfn algorithm which constructs PFNs.
* `path_gen.py` - contains the Jlab SURL algorithm.
* `extract_scope.py` - contains the Jlab SCOPE algorithm.
* `permission.py` - permission functions for the policy package.
* `schema.py` - schema functions and data for the policy package.

## How to use this policy package

*  Make sure the directory containing the `jlab_rucio_policy_package` is in the PYTHONPATH for the Rucio server.
*  Set following in the `[policy]` section of rucio cfg.
     ```
     package = jlab_rucio_policy_package
     extract_scope= jlab
     ```
