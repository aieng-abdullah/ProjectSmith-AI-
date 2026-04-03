import { auth } from "@/auth";
import { redirect } from "next/navigation";
import { ChatInterface } from "@/components/chat-interface";

export default async function ChatPage() {
  const session = await auth();

  if (!session?.user) {
    redirect("/login");
  }

  return <ChatInterface user={session.user} />;
}
