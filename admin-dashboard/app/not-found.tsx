import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="flex h-screen w-full flex-col items-center justify-center space-y-4 bg-background">
      <h2 className="text-3xl font-bold">404</h2>
      <p className="text-muted-foreground">Page not found</p>
      <Link href="/" className="text-primary hover:underline">
        Return to Dashboard
      </Link>
    </div>
  );
}