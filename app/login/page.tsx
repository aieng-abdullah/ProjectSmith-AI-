import { auth } from "@/auth";
import { redirect } from "next/navigation";
import { LoginForm } from "@/components/login-form";

// Check if Google OAuth is configured
const isAuthConfigured = !!(
  process.env.GOOGLE_CLIENT_ID && 
  process.env.GOOGLE_CLIENT_SECRET &&
  process.env.AUTH_SECRET
);

export default async function LoginPage() {
  // Demo mode: redirect to chat if auth is not configured
  if (!isAuthConfigured) {
    redirect("/chat");
  }

  const session = await auth();

  if (session?.user) {
    redirect("/chat");
  }

  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-background">
      <div className="w-full max-w-md px-6">
        <LoginForm />
      </div>
    </main>
  );
}
