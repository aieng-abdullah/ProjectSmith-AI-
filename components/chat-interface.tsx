"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { signOut } from "next-auth/react";
import { v4 as uuidv4 } from "uuid";
import {
  Hammer,
  Send,
  Plus,
  LogOut,
  Loader2,
  Sparkles,
  FileText,
  DollarSign,
  AlertTriangle,
  ChevronRight,
  User,
  Bot,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Separator } from "@/components/ui/separator";
import { Sidebar } from "@/components/sidebar";
import { PlanResult } from "@/components/plan-result";
import { sendMessage, generatePlan, type PlanResponse } from "@/lib/api";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

interface ChatInterfaceProps {
  user: {
    id?: string;
    name?: string | null;
    email?: string | null;
    image?: string | null;
  };
}

const PLAN_TRIGGERS = [
  "plan it",
  "plan this",
  "build it",
  "let's plan",
  "lets plan",
  "go",
  "start planning",
];

export function ChatInterface({ user }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [threadId, setThreadId] = useState(() => uuidv4());
  const [planResult, setPlanResult] = useState<PlanResponse | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const scrollRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const userId = user.email || user.id || "anonymous";

  const scrollToBottom = useCallback(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  const handleNewChat = useCallback(() => {
    setMessages([]);
    setThreadId(uuidv4());
    setPlanResult(null);
    inputRef.current?.focus();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: uuidv4(),
      role: "user",
      content: input.trim(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    const isPlanTrigger = PLAN_TRIGGERS.some((trigger) =>
      input.toLowerCase().includes(trigger)
    );

    try {
      if (isPlanTrigger) {
        // Planning flow
        const result = await generatePlan(userId, threadId, input);
        setPlanResult(result);

        setMessages((prev) => [
          ...prev,
          {
            id: uuidv4(),
            role: "assistant",
            content:
              "Your project plan is ready! Check out the detailed breakdown below.",
          },
        ]);
      } else {
        // Regular chat flow
        const response = await sendMessage(userId, threadId, input);

        setMessages((prev) => [
          ...prev,
          {
            id: uuidv4(),
            role: "assistant",
            content:
              response.response || "Sorry, I couldn't generate a response.",
          },
        ]);
      }
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          id: uuidv4(),
          role: "assistant",
          content:
            "Sorry, there was an error connecting to the server. Please make sure the API is running.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <Sidebar
        isOpen={sidebarOpen}
        onToggle={() => setSidebarOpen(!sidebarOpen)}
        onNewChat={handleNewChat}
        user={user}
        userId={userId}
      />

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <header className="h-14 border-b border-border flex items-center justify-between px-4">
          <div className="flex items-center gap-3">
            {!sidebarOpen && (
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setSidebarOpen(true)}
                className="lg:hidden"
              >
                <ChevronRight className="h-5 w-5" />
              </Button>
            )}
            <div className="flex items-center gap-2">
              <Hammer className="h-5 w-5 text-foreground" />
              <span className="font-semibold text-foreground">
                ProjectSmith AI
              </span>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-sm text-muted-foreground hidden sm:block">
              {user.name || user.email}
            </span>
            <Avatar className="h-8 w-8">
              <AvatarImage src={user.image || undefined} alt={user.name || "User"} />
              <AvatarFallback>
                {user.name?.charAt(0).toUpperCase() || "U"}
              </AvatarFallback>
            </Avatar>
          </div>
        </header>

        {/* Messages Area */}
        <ScrollArea className="flex-1" ref={scrollRef}>
          <div className="max-w-3xl mx-auto px-4 py-6">
            {messages.length === 0 ? (
              <WelcomeScreen onSuggestionClick={setInput} />
            ) : (
              <div className="space-y-6">
                {messages.map((message) => (
                  <MessageBubble key={message.id} message={message} user={user} />
                ))}

                {isLoading && (
                  <div className="flex gap-4">
                    <div className="flex items-center justify-center w-8 h-8 rounded-full bg-primary">
                      <Bot className="w-4 h-4 text-primary-foreground" />
                    </div>
                    <div className="flex items-center gap-2 text-muted-foreground">
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span>Thinking...</span>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Plan Result */}
            {planResult && <PlanResult result={planResult} />}
          </div>
        </ScrollArea>

        {/* Input Area */}
        <div className="border-t border-border p-4">
          <form
            onSubmit={handleSubmit}
            className="max-w-3xl mx-auto relative"
          >
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Describe your startup idea... (Type 'plan it' when ready)"
              className="w-full min-h-[52px] max-h-[200px] resize-none rounded-xl border border-input bg-card px-4 py-3 pr-12 text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
              rows={1}
              disabled={isLoading}
            />
            <Button
              type="submit"
              size="icon"
              disabled={!input.trim() || isLoading}
              className="absolute right-2 bottom-2 h-9 w-9 rounded-lg"
            >
              {isLoading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Send className="h-4 w-4" />
              )}
            </Button>
          </form>
          <p className="text-center text-xs text-muted-foreground mt-3">
            AI-generated advice. Always validate with real experts before
            taking action.
          </p>
        </div>
      </div>
    </div>
  );
}

function WelcomeScreen({
  onSuggestionClick,
}: {
  onSuggestionClick: (text: string) => void;
}) {
  const suggestions = [
    "I want to build an app for local farmers to sell directly to consumers",
    "Help me validate my SaaS idea for project management",
    "I have an idea for an AI tutoring platform for students",
  ];

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
      <div className="flex items-center justify-center w-16 h-16 rounded-2xl bg-primary mb-6">
        <Hammer className="w-8 h-8 text-primary-foreground" />
      </div>
      <h2 className="text-2xl font-bold text-foreground mb-2">
        Welcome to ProjectSmith AI
      </h2>
      <p className="text-muted-foreground mb-8 max-w-md">
        Tell me about your startup idea. I&apos;ll challenge your assumptions,
        help you validate it, and create a detailed project plan when
        you&apos;re ready.
      </p>

      <div className="grid gap-3 w-full max-w-md">
        {suggestions.map((suggestion, index) => (
          <button
            key={index}
            onClick={() => onSuggestionClick(suggestion)}
            className="p-4 text-left rounded-lg border border-border bg-card hover:bg-accent transition-colors text-sm text-foreground"
          >
            {suggestion}
          </button>
        ))}
      </div>

      <div className="mt-8 flex flex-wrap justify-center gap-4 text-xs text-muted-foreground">
        <span className="flex items-center gap-1">
          <Sparkles className="w-3 h-3" /> Idea Validation
        </span>
        <span className="flex items-center gap-1">
          <FileText className="w-3 h-3" /> Project Planning
        </span>
        <span className="flex items-center gap-1">
          <DollarSign className="w-3 h-3" /> Cost Analysis
        </span>
        <span className="flex items-center gap-1">
          <AlertTriangle className="w-3 h-3" /> Risk Assessment
        </span>
      </div>
    </div>
  );
}

function MessageBubble({
  message,
  user,
}: {
  message: Message;
  user: ChatInterfaceProps["user"];
}) {
  const isUser = message.role === "user";

  return (
    <div className="flex gap-4">
      {isUser ? (
        <Avatar className="h-8 w-8 shrink-0">
          <AvatarImage src={user.image || undefined} alt={user.name || "User"} />
          <AvatarFallback>
            <User className="w-4 h-4" />
          </AvatarFallback>
        </Avatar>
      ) : (
        <div className="flex items-center justify-center w-8 h-8 rounded-full bg-primary shrink-0">
          <Bot className="w-4 h-4 text-primary-foreground" />
        </div>
      )}
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-foreground mb-1">
          {isUser ? user.name || "You" : "ProjectSmith"}
        </p>
        <div className="text-foreground leading-relaxed whitespace-pre-wrap">
          {message.content}
        </div>
      </div>
    </div>
  );
}
