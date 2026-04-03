import { auth } from "@/auth";

export default auth((req) => {
  const isLoggedIn = !!req.auth;
  const isOnChat = req.nextUrl.pathname.startsWith("/chat");

  if (isOnChat && !isLoggedIn) {
    return Response.redirect(new URL("/login", req.nextUrl));
  }
});

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
