# cohdl_yosys

cohdl_yosys is a small Python library that adds formal verification support to the [CoHDL](https://github.com/alexander-forster/cohdl) hardware description language. 

It consists of two main components:

* a module of utility functions to describe formal properties of hardware designs

    These functions use the inline code feature of CoHDL to embed PSL statements into the generated VHDL representation.
    
* an abstaction layer to define SymbiYosys projects as Python classes

    The verification tools can either be invoked directly or via the Python unittest module. This allows for easy test automation and IDE integration.

The library is not limited to CoHDL designs. It is also possible to verify VHDL code.

## documentation

The documentation of cohdl_yosys can be found in the [cohdl_documentation](https://github.com/alexander-forster/cohdl_documentation) repo.

## installation

cohdl_yosys itself is available as a pip package and can installed with:

```
pip install cohdl_yosys
```

Since the library relies on [GHDL](https://github.com/ghdl/ghdl), [SymbiYosys](https://github.com/YosysHQ/sby) and the [ghdl-yosys-plugin](https://github.com/ghdl/ghdl-yosys-plugin) to perform the actual verification, these components and their dependencies need to be installed too. You can use the Dockerfile in the [cohdl_documentation](https://github.com/alexander-forster/cohdl_documentation) repo as a reference or work with the cohdl docker image directly.