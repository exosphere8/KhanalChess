# TypeScript decision record

Status: decided. Date: 2026-11-18. Updated: 2026-11-22, after the owner's
decision of 2026-11-19 to switch.

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

## Decision

1. Switch to TypeScript after the backend is finished. The backend comes
   first, because the frontend screens depend on it.
2. Change every frontend JavaScript file to TypeScript in one PR on its own
   branch.
3. That PR updates this record if anything changes.

## Reasons

- The backend sign-in work is the current priority.
- The cost of switching grows with every JavaScript screen added.

## Trade-offs

- Waiting means a larger migration than switching today.
- A type checker in CI is one more job to keep fast and green.

## Not decided

What counts as a finished backend: the sign-in endpoints and log out, or
also the game engine.

## Not checked

How Vite, Vitest and ESLint are set up for TypeScript in this repository,
and what the migration would change in CI. To be read from their own
documentation before the switch.

## Out of scope

Changing the backend language, and any other frontend framework.
