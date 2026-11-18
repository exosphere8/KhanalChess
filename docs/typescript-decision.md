# TypeScript decision record

Status: proposed. Date: 2026-11-18. The switch is parked, not rejected.

## Context

The frontend is React with Vite, written in JavaScript. It is small: the
opening menu, the SVG bishop logo and one test. A friend who is a frontend
developer suggested TypeScript because it scales more easily. Sign-in will
add data from the API (who is signed in), and later the game screen will
add more.

## Options

Stay with JavaScript for now
- No migration work while the frontend is small.
- Every new screen written in JavaScript has to be converted later.

Switch to TypeScript
- Types describe what each value is, so many mistakes show up before the
  code runs.
- The shape of API data can be written down once and checked everywhere.
- One migration PR, a little more to learn, and a type check in CI.

## Decision (proposed)

1. Park the switch for now. The backend sign-in endpoints come first,
   because the frontend screens depend on them.
2. Decide again before the frontend sign-up menu is built, while the
   frontend is still small.
3. If we switch, it is one PR on its own branch, with its own record update.

## Reasons

- The backend sign-in work is the current priority.
- The cost of switching grows with every JavaScript screen added.

## Trade-offs

- Waiting means a larger migration if we do switch.
- A type checker in CI is one more job to keep fast and green.

## Not checked

How Vite, Vitest and ESLint are set up for TypeScript in this repository,
and what the migration would change in CI. To be read from their own
documentation before the switch.

## Out of scope

Changing the backend language, and any other frontend framework.
