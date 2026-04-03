import { auth } from "@/auth";

// Check if Google OAuth is configured
const isAuthConfigured = !!(
  process.env.GOOGLE_CLIENT_ID && 
  process.env.GOOGLE_CLIENT_SECRET &&
  process.env.AUTH_SECRET
);

export default auth((req) => {
  // Skip auth check if OAuth is not configured (demo mode)
  if (!isAuthConfigured) {
    return;
  }

  const isLoggedIn = !!req.auth;
  const isOnChat = req.nextUrl.pathname.startsWith("/chat");

  if (isOnChat && !isLoggedIn) {
    return Response.redirect(new URL("/login", req.nextUrl));
  }
});

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
