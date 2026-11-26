import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import App from "./App.jsx";

afterEach(cleanup);

describe("App", () => {
  it("shows the title and the menu actions", () => {
    render(<App />);
    expect(screen.getByRole("heading", { name: "KhanalChess" })).toBeTruthy();
    for (const name of ["PLAY", "Continue with Google", "About Us"]) {
      expect(screen.getByRole("link", { name })).toBeTruthy();
    }
  });

  it("sends the Google button to the backend sign-in", () => {
    render(<App />);
    const link = screen.getByRole("link", { name: "Continue with Google" });
    expect(link.getAttribute("href")).toBe(
      "http://localhost:8000/auth/google/login",
    );
  });
});
