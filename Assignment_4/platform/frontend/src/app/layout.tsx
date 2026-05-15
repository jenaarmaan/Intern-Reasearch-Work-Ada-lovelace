import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Luminary AI | Controlled Generation",
  description: "Advanced Stable Diffusion platform with ControlNet integration",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
