import { test, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import Navbar from "../components/Navbar";

test("renders portal title", () => {
  render(
    <BrowserRouter>
      <Navbar />
    </BrowserRouter>
  );

  expect(
    screen.getByText("Campus Health Portal")
  ).toBeInTheDocument();
});

test("renders navigation links", () => {
  render(
    <BrowserRouter>
      <Navbar />
    </BrowserRouter>
  );

  expect(
    screen.getByText("Dashboard")
  ).toBeInTheDocument();

  expect(
    screen.getByText("Login")
  ).toBeInTheDocument();
});