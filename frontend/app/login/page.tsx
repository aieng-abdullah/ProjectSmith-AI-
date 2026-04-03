import { auth } from "@/auth";
import { redirect } from "next/navigation";
import { LoginForm } from "@/components/login-form";

export default async function LoginPage() {
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
