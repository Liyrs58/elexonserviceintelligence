import Link from 'next/link';
import { Activity, ArrowUpRight } from 'lucide-react';
import { nav } from '@/lib/canonical';

export function SiteShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-[#f5f7f8] text-[#17262c]">
      <header className="sticky top-0 z-50 border-b border-slate-200/90 bg-white/95 backdrop-blur">
        <div className="mx-auto flex max-w-[1440px] items-center justify-between gap-6 px-5 py-4 lg:px-10">
          <Link href="/" className="flex min-w-0 items-center gap-3">
            <span className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-[#102e3a] text-white"><Activity size={21} strokeWidth={2} /></span>
            <span className="min-w-0">
              <span className="block truncate text-sm font-bold tracking-tight">Settlement Intelligence</span>
              <span className="block truncate text-[11px] font-medium uppercase tracking-[0.16em] text-slate-500">Independent portfolio project</span>
            </span>
          </Link>
          <nav className="hidden items-center gap-1 xl:flex" aria-label="Main navigation">
            {nav.map((item) => <Link key={item.href} href={item.href} className="rounded-lg px-3 py-2 text-sm font-medium text-slate-600 transition hover:bg-slate-100 hover:text-[#102e3a]">{item.label}</Link>)}
          </nav>
          <Link href="/downloads" className="inline-flex shrink-0 items-center gap-2 rounded-lg bg-[#0d7480] px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-[#095e68]">Review files <ArrowUpRight size={16} /></Link>
        </div>
        <nav className="flex gap-1 overflow-x-auto border-t border-slate-100 px-4 py-2 xl:hidden" aria-label="Mobile navigation">
          {nav.map((item) => <Link key={item.href} href={item.href} className="whitespace-nowrap rounded-md px-3 py-1.5 text-xs font-semibold text-slate-600 hover:bg-slate-100">{item.label}</Link>)}
        </nav>
      </header>
      {children}
      <footer className="border-t border-slate-200 bg-white">
        <div className="mx-auto grid max-w-[1440px] gap-6 px-5 py-10 text-sm text-slate-600 md:grid-cols-[1fr_auto] lg:px-10">
          <div><p className="font-semibold text-[#17262c]">GB Settlement & Imbalance Service Intelligence Monitor</p><p className="mt-2 max-w-2xl">An independent analysis of public Elexon data. It is not affiliated with or endorsed by Elexon and is not an operational market service.</p></div>
          <div className="md:text-right"><p className="font-semibold text-[#17262c]">Canonical scope</p><p className="mt-2">Q4 2025 · 1 October–31 December</p></div>
        </div>
      </footer>
    </div>
  );
}

export function PageIntro({ eyebrow, title, copy }: { eyebrow: string; title: string; copy: string }) {
  return <div className="max-w-4xl"><p className="eyebrow">{eyebrow}</p><h1 className="mt-4 text-balance text-4xl font-bold tracking-[-0.04em] text-[#102e3a] md:text-6xl">{title}</h1><p className="mt-6 max-w-3xl text-lg leading-8 text-slate-600">{copy}</p></div>;
}
