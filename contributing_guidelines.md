# Contributing Guidelines


### Language to use is English

## Organisation

Issues and work time will be tracked by Jira.
If you want to contribute to the project send an email to one of the project managers.

## Timetracking

The amount of work put into this project is to be documented. For that purpose there is a time sheet on the Jira portal.
The amount of time per work segment is not to be more then 4 hours. Everything longer should be split into smaller segments.

## Issues

A general guide on how to create issues for this project.

### When to create an Issue

Issues should generally be used as soon as a new **feature** is planned to be implemented or a **bug** is reported that needs fixing.

Issues should be created by everyone with the following routine.

1. **Check the existing issues**, there should never be a duplicate issue.
2. Create the issue following the **styleguide**.
3. **Tag the issue** with appropriate tags.

If an issue is implementing a feature it should always be connected to its epic. Unless it is a bug(fix).

### Styleguide

**Titel:**

The title of the Issue should always be **short but descriptive**.
It should always tell everyone clearly what the core idea of this issue is by following a simple grammar and the **imperative mood in the present tense.** A contributer without code knowledge should be able to read the **title** of the issue, details can follow in the description.

 Examples:

```txt
"Implement submit button on comments"
"Remove loose dependencies"
"Fix access control of database xy"
```
---

**Bad** examples:

```txt
"Adding logs" # no context (logs for what?)
"Had problem with login, fixing later" # Too little information about bug
"Fix Function xy, is returning ab" # Too specific, details belong in the description
```

**Description:**

In the description of the issue describe the **feature** in more detail. Name specific tools and methods on how the feature is planned to be implemented. Pictures of mock ups and graphs are good tools to make the issue more detailed.
If the issue is tracking a **bug** it should have a description on how to reproduce the bug, if possible. Screenshots, logs, error messages and potential fixes are encouraged as well.

## Branches

Branches should follow the style of:

~~~txt
feature/<NAME>
docu/<NAME>
fix/<NAME>
release/<NAME>
misc/<NAME>
~~~

### Merge requests

Merge requests should always be approved by at least another person in the project.

## Commits

Commits should follow a similar style as Issues.

Examples:

~~~txt
"Add Submit button on comments"
"Resize header font"
"Fix login form"
~~~

## Lables

Always select lables for the issue you are creating. 
