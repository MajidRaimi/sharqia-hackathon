"use client";

import { type ButtonHTMLAttributes } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
}

export function Button({ children, ...props }: ButtonProps) {
  return (
    <button
      style={{
        padding: "0.5rem 1rem",
        borderRadius: "0.375rem",
        border: "1px solid #e5e7eb",
        backgroundColor: "#111",
        color: "#fff",
        cursor: "pointer",
        fontSize: "0.875rem",
        fontWeight: 500,
      }}
      {...props}
    >
      {children}
    </button>
  );
}
