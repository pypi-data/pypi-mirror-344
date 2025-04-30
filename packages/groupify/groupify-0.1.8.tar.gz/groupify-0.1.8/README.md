# `groupify`
`groupify` is a Python package for automatically creating random groups in the classroom from a classlist. 

> NOTE: there is currently no way to ensure that Newton and Leibniz are not in the same group. They must cooperate if necessary.


## Installation

To install on Unix/Linux:

```bash
pip install groupify
```

To install in an IDE simply search for the package `groupify` and install it.

## Basic examples

### Example 1

```python
import groupify

classlist = "sample_class.txt"

groupify.create(
    classlist=classlist,
    group_size=4,
)

groupify.savefig(dirname="../figures/", fname="example_1.svg")

groupify.show()
```

This will generate the following groups (randomly):

![example 1](https://raw.githubusercontent.com/reneaas/groupify/refs/heads/main/examples/figures/example_1.svg)


### Example 2

If some students are absent, you can specify them in the `absent` parameter to exclude them from the list of students before creating the groups.

```python
import groupify

classlist = "sample_class.txt"

absent = [
    "Einstein",  # Busy dreaming about light
    "Feynman",  # Busy pick-locking government secrets
    "Hilbert",  # Busy trying to one-up Einstein on GR
    "Schrödinger",  # Uncertain if he's here or not – we'll exlude him to be sure
]

groupify.create(
    classlist=classlist,
    group_size=4,
    absent=absent,  # Removes them from the list before creating the groups
)

groupify.savefig(dirname="../figures/", fname="example_2.svg")

groupify.show()
```

This will generate the following groups (randomly):

![example 2](https://raw.githubusercontent.com/reneaas/groupify/refs/heads/main/examples/figures/example_2.svg)




### Example 3

```python
import groupify

classlist = "sample_class.txt"

groupify.create(
    classlist=classlist,
    group_size=3,
)

groupify.savefig(dirname="../figures/", fname="example_3.svg")

groupify.show()
```

This will generate the following groups (randomly):

![example 3](https://raw.githubusercontent.com/reneaas/groupify/refs/heads/main/examples/figures/example_3.svg)


### Example 4

```python
import groupify

classlist = "sample_class.txt"

groupify.create(
    classlist=classlist,
    group_size=2,
)

groupify.savefig(dirname="../figures/", fname="example_4.svg")

groupify.show()
```

This will generate the following groups (randomly):

![example 4](https://raw.githubusercontent.com/reneaas/groupify/refs/heads/main/examples/figures/example_4.svg)