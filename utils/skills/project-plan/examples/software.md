# Software development

Planning on software should follow this pattern:

In any of the following, any questions or ambiguities
should be asked and discussed before planning anything.

First -- architecture / interfaces

It's very important that the first output is a detailed 
description of the interfaces of the plan. Interfaces could be
very high level (i.e. what a user would see), or low level
(i.e. a function in the code), depending on the existing codebase.

Second -- implementation isolation

If there's work to implement, it's very important to separate
using the defined interfaces as a boundary. E.g., the task of
implementing some interface and the task of using that interface
for some other thing should not depend on each other. Furthermore,
those two tasks could be delegated to independent agents.

## Examples
