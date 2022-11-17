# HW3 Part 2: Normalization

# Solutions
 * Edit 11/17: Key `category` added to Q2.1

## Warmup:
Trivial functional dependencies are those where the right side is included on the left. For example: ABC->C

To derive additional functional dependencies, we can use Armstrong's Axioms:
- Augment the existing functional dependencies by adding attributes to both sides.
- Apply transitivity to other functional dependencies.

**Q1.1**
  * Non trivial functional dependencies (in addition to given FDs): AB->C
  * Keys: AB


**Q1.2**
  * Non trivial functional dependencies (in addition to given FDs):
    - ACD->B,
    - ABC->D,
    - BCD->A,
    - AC->B,
    - CD->A

  * Keys: AC, CD

# Real application:
**Q2.1**

Key in `iowa` -
`(store, itemno, date, vendor_no, invoice_line_no, category)`


**Q2.2**

**False.** The constraint given in the question is a check constraint, that only involves the value of a single column. Functional dependencies cannot enforce check constraints. They can only enforce a relationship between the values in two or more columns.


**Q2.3** `select distinct(name) from iowa where store = 2508;`

**Result:**

  We find only one name: `Hy-Vee Food Store #1 / Cedar Rapids`, so the answer is 1

**Q2.4**

**No,** the `store` and `name` should not have a functional dependency. The design of the database may seem that the `store` uniquely identifies a `name`, meaning one `name` name given a `store` number. However, it may also be possible for stores to change their names

**Yes,** the `store` and `name` should be a functional dependency. Given the previous question and the design of the database, each `store` uniquely identifies a `name`, meaning one `name` name given a `store` number.
