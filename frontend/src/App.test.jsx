import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import App from "./App.jsx";

afterEach(cleanup);

describe("App", () => {
  it("shows the title and the menu actions", () => {
    render(<App />);
    expect(screen.getByRole("heading", { name: "KhanalChess" })).toBeTruthy();
    for (const name of ["PLAY", "Sign up", "Login", "About Us"]) {
      expect(screen.getByRole("link", { name })).toBeTruthy();
    }
  });
});
