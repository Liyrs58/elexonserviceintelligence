import type { Metadata } from 'next';
import { Download, FileArchive, FileChartColumn, FileSpreadsheet, Presentation } from 'lucide-react';
import { PageIntro, SiteShell } from '@/components/site-shell';

export const metadata: Metadata = { title: 'Downloads' };

const downloads = [
  { href: '/downloads/service-insight-note.pdf', title: 'Service Insight Note', detail: 'One-page PDF · Q4 2025 findings and next checks', icon: FileChartColumn },
  { href: '/downloads/presentation.pdf', title: 'Presentation PDF', detail: 'Eight reviewed pages · recruiter-ready narrative', icon: Presentation },
  { href: '/downloads/presentation.pptx', title: 'Editable presentation', detail: 'PowerPoint source · editable charts and evidence grids', icon: Presentation },
  { href: '/downloads/powerbi-review-package.zip', title: 'Power BI reviewer package', detail: 'PBIP/PBIR/TMDL, required data, previews, checksums and QA checklist', icon: FileArchive },
  { href: '/downloads/exception-queue.csv', title: 'Exception queue', detail: '130 canonical Q4 review records · CSV', icon: FileSpreadsheet },
  { href: '/downloads/daily-summary.csv', title: 'Daily summary', detail: '92-day canonical Q4 summary · CSV', icon: FileSpreadsheet },
  { href: '/downloads/length-summary.csv', title: 'System-length summary', detail: 'Short, long and balanced comparison · CSV', icon: FileSpreadsheet },
  { href: '/downloads/version-reconciliation.md', title: 'Version reconciliation', detail: 'Canonical decision and exact 130-versus-124 explanation · Markdown', icon: FileChartColumn },
];

export default function DownloadsPage() {
  return (
    <SiteShell>
      <main className="mx-auto max-w-[1440px] px-5 py-16 lg:px-10 lg:py-20">
        <PageIntro eyebrow="Project files" title="Open the work, not just a README." copy="The core recruiter artifacts, Power BI handoff package and selected analysis sheets are available directly. All numerical material uses the canonical Q4 2025 population." />
        <div className="mt-12 grid gap-5 md:grid-cols-2 xl:grid-cols-3">
          {downloads.map(({ href, title, detail, icon: Icon }) => <a key={href} href={href} download className="group flex min-h-44 flex-col rounded-2xl border border-slate-200 bg-white p-6 transition hover:-translate-y-0.5 hover:border-teal-300 hover:shadow-lg"><div className="flex items-start justify-between"><span className="grid h-11 w-11 place-items-center rounded-xl bg-teal-50 text-[#0d7480]"><Icon size={22} /></span><Download className="text-slate-400 transition group-hover:text-[#0d7480]" size={19} /></div><h2 className="mt-7 text-lg font-bold text-[#102e3a]">{title}</h2><p className="mt-2 text-sm leading-6 text-slate-500">{detail}</p></a>)}
        </div>
        <div className="mt-12 rounded-2xl border border-amber-200 bg-amber-50 p-6 text-sm leading-7 text-amber-950"><strong>Power BI handoff:</strong> the ZIP is intended for a licensed Windows reviewer. Open the PBIP, set the DataFolder parameter, refresh, verify all 19 measures, test interactions and replace the four static previews only after genuine runtime QA passes.</div>
      </main>
    </SiteShell>
  );
}
