"use client";

import { signIn } from "next-auth/react";
import { Hammer, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";

export function LoginForm() {
  return (
    <div className="flex flex-col items-center gap-8">
      {/* Logo and Title */}
      <div className="flex flex-col items-center gap-4">
        <div className="flex items-center justify-center w-16 h-16 rounded-2xl bg-primary">
          <Hammer className="w-8 h-8 text-primary-foreground" />
        </div>
        <div className="text-center">
          <h1 className="text-3xl font-bold tracking-tight text-foreground">
            ProjectSmith AI
          </h1>
          <p className="mt-2 text-muted-foreground">
            Your intelligent startup advisor
          </p>
        </div>
      </div>

      {/* Features */}
      <div className="flex flex-col gap-3 w-full">
        <Feature text="Challenge assumptions and validate your idea" />
        <Feature text="Generate project plans and cost breakdowns" />
        <Feature text="Identify edge cases and risks early" />
        <Feature text="Export professional project briefs" />
      </div>

      {/* Sign In Button */}
      <div className="w-full space-y-4">
        <Button
          onClick={() => signIn("google", { callbackUrl: "/chat" })}
          className="w-full h-12 gap-3 text-base font-medium"
        >
          <GoogleIcon />
          Continue with Google
        </Button>
        <p className="text-center text-xs text-muted-foreground">
          By continuing, you agree to our Terms of Service and Privacy Policy
        </p>
      </div>

      {/* Disclaimer */}
      <div className="p-4 rounded-lg bg-muted/50 border border-border">
        <p className="text-xs text-muted-foreground text-center leading-relaxed">
          ProjectSmith is an AI tool for ideation only. Do not share sensitive
          business information. Always validate AI advice with qualified
          professionals.
        </p>
      </div>
    </div>
  );
}

function Feature({ text }: { text: string }) {
  return (
    <div className="flex items-center gap-3 px-4 py-3 rounded-lg bg-card border border-border">
      <Sparkles className="w-4 h-4 text-muted-foreground shrink-0" />
      <span className="text-sm text-foreground">{text}</span>
    </div>
  );
}

function GoogleIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24">
      <path
        fill="currentColor"
        d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
      />
      <path
        fill="currentColor"
        d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
      />
      <path
        fill="currentColor"
        d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
      />
      <path
        fill="currentColor"
        d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
      />
    </svg>
  );
}
