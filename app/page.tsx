import Link from "next/link";
import {
  Hammer,
  Sparkles,
  FileText,
  DollarSign,
  AlertTriangle,
  ArrowRight,
  MessageSquare,
  Zap,
} from "lucide-react";
import { Button } from "@/components/ui/button";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-background">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        {/* Background glow effect */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[600px] bg-primary/5 rounded-full blur-3xl" />

        <div className="relative max-w-5xl mx-auto px-6 pt-20 pb-32">
          {/* Header */}
          <header className="flex items-center justify-between mb-20">
            <div className="flex items-center gap-2">
              <Hammer className="h-6 w-6 text-foreground" />
              <span className="font-semibold text-lg text-foreground">
                ProjectSmith
              </span>
            </div>
            <Link href="/chat">
              <Button variant="outline" className="gap-2">
                Start Chatting
                <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
          </header>

          {/* Hero Content */}
          <div className="text-center max-w-3xl mx-auto">
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-foreground text-balance">
              Ship your startup idea with confidence.
            </h1>
            <p className="mt-6 text-lg text-muted-foreground leading-relaxed max-w-2xl mx-auto text-pretty">
              ProjectSmith AI is an intelligent advisor that challenges your
              assumptions, validates your idea, and generates comprehensive
              project plans. Not a chatbot that just answers questions.
            </p>
            <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link href="/chat">
                <Button size="lg" className="gap-2 h-12 px-8">
                  Get Started
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <section className="py-20 border-t border-border">
        <div className="max-w-5xl mx-auto px-6">
          <h2 className="text-2xl font-bold text-foreground text-center mb-12">
            What ProjectSmith does differently
          </h2>

          <div className="grid md:grid-cols-2 gap-6">
            <FeatureCard
              icon={MessageSquare}
              title="Conversational Validation"
              description="Challenges your assumptions and pushes for specifics before any planning begins. Like having a senior advisor in your pocket."
            />
            <FeatureCard
              icon={Sparkles}
              title="4-Node Planning Pipeline"
              description="Planner, cost advisor, edge case finder, and PRD generator run sequentially to create a comprehensive project brief."
            />
            <FeatureCard
              icon={DollarSign}
              title="Live Cost Analysis"
              description="Fetches real-time pricing data to recommend free tools you can start with and future costs as you scale."
            />
            <FeatureCard
              icon={AlertTriangle}
              title="Risk Assessment"
              description="Identifies critical edge cases specific to your project with actionable fixes before you start building."
            />
          </div>
        </div>
      </section>

      {/* Example Section */}
      <section className="py-20 border-t border-border bg-card/50">
        <div className="max-w-3xl mx-auto px-6">
          <h2 className="text-2xl font-bold text-foreground text-center mb-8">
            See it in action
          </h2>

          <div className="rounded-xl border border-border bg-card p-6 space-y-4 font-mono text-sm">
            <Message role="user">
              I want to build an app where farmers sell directly to customers
            </Message>
            <Message role="assistant">
              What stops a farmer from just using WhatsApp groups they already
              have?
            </Message>
            <Message role="user">
              Because they lose 40% to middlemen and we only take 5%
            </Message>
            <Message role="assistant">
              What concrete evidence do you have that a farmer would move
              platforms for that?
            </Message>
            <Message role="user">plan it</Message>
            <Message role="assistant" highlight>
              Generating plan... cost... edge cases... project brief...
            </Message>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 border-t border-border">
        <div className="max-w-3xl mx-auto px-6 text-center">
          <div className="flex items-center justify-center w-14 h-14 rounded-2xl bg-primary mx-auto mb-6">
            <Zap className="w-7 h-7 text-primary-foreground" />
          </div>
          <h2 className="text-2xl font-bold text-foreground mb-4">
            Ready to validate your idea?
          </h2>
          <p className="text-muted-foreground mb-8">
            Start a conversation and get your project plan in minutes.
          </p>
          <Link href="/chat">
            <Button size="lg" className="gap-2">
              Get Started Free
              <ArrowRight className="h-4 w-4" />
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-border">
        <div className="max-w-5xl mx-auto px-6">
          <p className="text-center text-sm text-muted-foreground">
            ProjectSmith AI is for ideation purposes only. Always consult
            qualified professionals before making business decisions.
          </p>
        </div>
      </footer>
    </main>
  );
}

function FeatureCard({
  icon: Icon,
  title,
  description,
}: {
  icon: React.ElementType;
  title: string;
  description: string;
}) {
  return (
    <div className="p-6 rounded-xl border border-border bg-card">
      <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-muted mb-4">
        <Icon className="w-5 h-5 text-foreground" />
      </div>
      <h3 className="font-semibold text-foreground mb-2">{title}</h3>
      <p className="text-sm text-muted-foreground leading-relaxed">
        {description}
      </p>
    </div>
  );
}

function Message({
  role,
  children,
  highlight,
}: {
  role: "user" | "assistant";
  children: React.ReactNode;
  highlight?: boolean;
}) {
  return (
    <div
      className={`flex gap-3 ${role === "user" ? "justify-end" : "justify-start"}`}
    >
      <div
        className={`max-w-[80%] rounded-lg px-4 py-2 ${
          role === "user"
            ? "bg-primary text-primary-foreground"
            : highlight
              ? "bg-accent text-accent-foreground"
              : "bg-muted text-foreground"
        }`}
      >
        {children}
      </div>
    </div>
  );
}
