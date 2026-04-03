import { auth } from "@/auth";
import { redirect } from "next/navigation";
import { ChatInterface } from "@/components/chat-interface";

// Check if Google OAuth is configured
const isAuthConfigured = !!(
  process.env.GOOGLE_CLIENT_ID && 
  process.env.GOOGLE_CLIENT_SECRET &&
  process.env.AUTH_SECRET
);

export default async function ChatPage() {
  const session = await auth();

  // Demo mode: allow access without auth
  if (!isAuthConfigured) {
    const demoUser = {
      name: "Demo User",
      email: "demo@projectsmith.ai",
      image: null,
    };
    return <ChatInterface user={demoUser} />;
  }

  if (!session?.user) {
    redirect("/login");
  }

  return <ChatInterface user={session.user} />;
}
