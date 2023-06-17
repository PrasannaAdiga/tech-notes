# Packaging
https://github.com/ardanlabs/gotraining/tree/master/topics/go/design/packaging

Package Oriented Design allows a developer to identify where a package belongs inside a Go project and the design guidelines the package must respect. It defines what a Go project is and how a Go project is structured. Finally, it improves communication between team members and promotes clean package design and project architecture that is discussable.

### Language Mechanics

- Packaging directly conflicts with how we have been taught to organize source code in other languages.
- In other languages, packaging is a feature that you can choose to use or ignore.
- You can think of packaging as applying the idea of microservices on a source tree.
- All packages are "first class," and the only hierarchy is what you define in the source tree for your project.
- There needs to be a way to “open” parts of the package to the outside world.
- Two packages can’t cross-import each other. Imports are a one way street.

### Design Philosophy

- To be purposeful, packages must provide, not contain.
- Packages must be named with the intent to describe what it provides.
- Packages must not become a dumping ground of disparate concerns.
- To be usable, packages must be designed with the user as their focus.
- Packages must be intuitive and simple to use.
- Packages must respect their impact on resources and performance.
- Packages must protect the user’s application from cascading changes.
- Packages must prevent the need for type assertions to the concrete.
- Packages must reduce, minimize and simplify its code base.
- To be portable, packages must be designed with reusability in mind.
- Packages must aspire for the highest level of portability.
- Packages must reduce setting policy when it’s reasonable and practical.
- Packages must not become a single point of dependency.

