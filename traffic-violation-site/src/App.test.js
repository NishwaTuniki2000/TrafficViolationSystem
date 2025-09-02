import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import App from "./App";

test("renders home page title", () => {
  render(
    <MemoryRouter>
      <App />
    </MemoryRouter>
  );

  const headingElement = screen.getByText(/Traffic Violation Detection System/i);
  expect(headingElement).toBeInTheDocument();
});
