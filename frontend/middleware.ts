import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Middleware runs on server, so we can't check localStorage
  // Route protection is handled by AuthContext on client side
  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/roadmap/:path*', '/daily-plan/:path*', '/learn/:path*', '/profile/:path*'],
};
