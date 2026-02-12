import { Button } from "@repo/ui/button";

export default function Home() {
  return (
    <main
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "100vh",
        gap: "1rem",
      }}
    >
      <h1>Sharqia Hackathon</h1>
      <Button>Get Started</Button>
    </main>
  );
}
