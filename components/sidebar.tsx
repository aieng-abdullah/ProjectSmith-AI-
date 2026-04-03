"use client";

import { useState, useEffect } from "react";
import { signOut } from "next-auth/react";
import useSWR from "swr";
import {
  Plus,
  LogOut,
  ChevronLeft,
  Clock,
  Trash2,
  MessageSquare,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { cn } from "@/lib/utils";

interface Memory {
  id: string;
  content: string;
  created_at: string;
}

interface SidebarProps {
  isOpen: boolean;
  onToggle: () => void;
  onNewChat: () => void;
  user: {
    name?: string | null;
    email?: string | null;
    image?: string | null;
  };
  userId: string;
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const fetcher = async (url: string) => {
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to fetch");
  const data = await res.json();
  return data.memories || [];
};

export function Sidebar({
  isOpen,
  onToggle,
  onNewChat,
  user,
  userId,
}: SidebarProps) {
  const { data: memories = [], mutate } = useSWR<Memory[]>(
    `${API_BASE}/memory/${userId}`,
    fetcher
  );

  const groupedMemories = groupByDate(memories);

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={onToggle}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          "fixed lg:static inset-y-0 left-0 z-50 w-72 bg-card border-r border-border flex flex-col transition-transform duration-200",
          isOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0 lg:w-0 lg:border-0"
        )}
      >
        <div className="flex items-center justify-between p-4 h-14">
          <span className="font-semibold text-foreground">History</span>
          <Button
            variant="ghost"
            size="icon"
            onClick={onToggle}
            className="lg:hidden"
          >
            <ChevronLeft className="h-5 w-5" />
          </Button>
        </div>

        <div className="px-3">
          <Button
            onClick={onNewChat}
            className="w-full justify-start gap-2"
            variant="outline"
          >
            <Plus className="h-4 w-4" />
            New Project
          </Button>
        </div>

        <Separator className="my-3" />

        <ScrollArea className="flex-1 px-3">
          {memories.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground text-sm">
              <MessageSquare className="h-8 w-8 mx-auto mb-2 opacity-50" />
              <p>No past sessions yet</p>
              <p className="text-xs mt-1">
                Start a conversation to see your history here
              </p>
            </div>
          ) : (
            <div className="space-y-4 pb-4">
              {Object.entries(groupedMemories).map(([group, items]) => (
                <div key={group}>
                  <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2 px-2">
                    {group}
                  </p>
                  <div className="space-y-1">
                    {items.map((memory) => (
                      <MemoryItem key={memory.id} memory={memory} />
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </ScrollArea>

        <Separator />

        {/* User Section */}
        <div className="p-3">
          <div className="flex items-center gap-3 p-2 rounded-lg">
            <Avatar className="h-8 w-8">
              <AvatarImage src={user.image || undefined} alt={user.name || "User"} />
              <AvatarFallback>
                {user.name?.charAt(0).toUpperCase() || "U"}
              </AvatarFallback>
            </Avatar>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-foreground truncate">
                {user.name}
              </p>
              <p className="text-xs text-muted-foreground truncate">
                {user.email}
              </p>
            </div>
          </div>
          <Button
            variant="ghost"
            className="w-full justify-start gap-2 mt-2 text-muted-foreground hover:text-foreground"
            onClick={() => signOut({ callbackUrl: "/login" })}
          >
            <LogOut className="h-4 w-4" />
            Sign Out
          </Button>
        </div>
      </aside>
    </>
  );
}

function MemoryItem({ memory }: { memory: Memory }) {
  const title = getMemoryTitle(memory.content);

  return (
    <button className="w-full text-left px-3 py-2 rounded-lg text-sm text-foreground hover:bg-accent transition-colors group">
      <div className="flex items-center gap-2">
        <MessageSquare className="h-4 w-4 text-muted-foreground shrink-0" />
        <span className="truncate">{title}</span>
      </div>
    </button>
  );
}

function getMemoryTitle(content: string): string {
  const firstLine = content.split("\n")[0].trim();
  return firstLine.length > 32 ? firstLine.slice(0, 32) + "..." : firstLine;
}

function groupByDate(memories: Memory[]): Record<string, Memory[]> {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);
  const weekAgo = new Date(today);
  weekAgo.setDate(weekAgo.getDate() - 7);

  const groups: Record<string, Memory[]> = {
    Today: [],
    Yesterday: [],
    "Previous 7 Days": [],
    Older: [],
  };

  const sorted = [...memories].sort(
    (a, b) =>
      new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
  );

  for (const memory of sorted) {
    const created = new Date(memory.created_at);
    created.setHours(0, 0, 0, 0);

    if (created.getTime() === today.getTime()) {
      groups.Today.push(memory);
    } else if (created.getTime() === yesterday.getTime()) {
      groups.Yesterday.push(memory);
    } else if (created >= weekAgo) {
      groups["Previous 7 Days"].push(memory);
    } else {
      groups.Older.push(memory);
    }
  }

  // Remove empty groups
  for (const key of Object.keys(groups)) {
    if (groups[key].length === 0) {
      delete groups[key];
    }
  }

  return groups;
}
