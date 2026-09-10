import type { Metadata } from 'next';
import Image from 'next/image';
import { ExternalLink } from 'lucide-react';
import { PageIntro, SiteShell } from '@/components/site-shell';
import { dashboardPages } from '@/lib/canonical';

export const metadata: Metadata = { title: 'Dashboard' };

export default function DashboardPage() {
  return (
    <SiteShell>
      <main className="mx-auto max-w-[1440px] px-5 py-16 lg:px-10 lg:py-20">
        <PageIntro eyebrow="Four-page Power BI design" title="A report organised around operational decisions." copy="These are data-bound static design previews generated from the canonical Q4 outputs and checked-in PBIR inventory. They are deliberately labelled as previews: live M refresh, DAX, filters, accessibility and performance still require licensed Power BI." />
        <div className="mt-12 rounded-xl border border-amber-200 bg-amber-50 px-5 py-4 text-sm leading-6 text-amber-950"><strong>Evidence boundary:</strong> these images show the intended information design and retained values. They are not Power BI runtime screenshots.</div>
        <div className="mt-10 space-y-12">
          {dashboardPages.map((page, index) => (
            <article key={page.slug} id={page.slug} className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
              <div className="grid gap-4 border-b border-slate-200 p-5 md:grid-cols-[80px_1fr_auto] md:items-center md:p-7">
                <div className="text-sm font-bold text-[#0d7480]">PAGE 0{index + 1}</div>
                <div><h2 className="text-2xl font-bold tracking-tight text-[#102e3a]">{page.title}</h2><p className="mt-1 text-slate-600">{page.decision}</p></div>
                <a href={page.image} target="_blank" className="inline-flex items-center gap-2 text-sm font-semibold text-[#0d7480]">Open full size <ExternalLink size={15} /></a>
              </div>
              <Image src={page.image} alt={`${page.title} static design preview`} width={1920} height={1080} className="h-auto w-full" priority={index === 0} />
            </article>
          ))}
        </div>
      </main>
    </SiteShell>
  );
}
