import { test, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import LoginPage from "../pages/LoginPage";

test("renders login heading", () => {
  render(<LoginPage />);

  expect(
    screen.getByText("Login")
  ).toBeInTheDocument();
});

test("renders login button", () => {
  render(<LoginPage />);

  expect(
    screen.getByRole("button")
  ).toBeInTheDocument();
});

test("shows login error message", () => {

  window.history.pushState(
    {},
    "",
    "/login?error=true"
  );

  render(<LoginPage />);

  expect(
    screen.getByText(
      "Login failed. Please try again."
    )
  ).toBeInTheDocument();
});