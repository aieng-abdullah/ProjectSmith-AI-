import { ChatInterface } from "@/components/chat-interface";

export default function ChatPage() {
  const user = {
    name: "User",
    email: "user@projectsmith.ai",
    image: null,
  };

  return <ChatInterface user={user} />;
}
