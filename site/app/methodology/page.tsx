import type { Metadata } from 'next';
import { AlertTriangle, CheckCircle2 } from 'lucide-react';
import { PageIntro, SiteShell } from '@/components/site-shell';

export const metadata: Metadata = { title: 'Methodology' };

export default function MethodologyPage() {
  return (
    <SiteShell>
      <main className="mx-auto max-w-[1440px] px-5 py-16 lg:px-10 lg:py-20">
        <PageIntro eyebrow="Audit trail" title="One canonical population. One unchanged method." copy="Q4 2025 is canonical because it is the successful run used by the semantic model, PBIR annotations, presentation, service note and dashboard previews." />
        <section className="mt-12 grid gap-6 lg:grid-cols-2">
          <div className="rounded-2xl border border-teal-200 bg-teal-50 p-7"><div className="flex items-center gap-3 text-[#0d7480]"><CheckCircle2 size={22} /><h2 className="text-xl font-bold">Q4 2025 · canonical</h2></div><p className="mt-5 leading-7 text-slate-700">1 October–31 December · 4,418 records · 2,076 short / 2,340 long / 2 balanced · 130 distinct flags.</p><div className="mt-6 grid gap-2 text-sm"><p><strong>Price p01/p99:</strong> −£11.22 / £153.8997</p><p><strong>|NIV| p99:</strong> 876.0417 MWh</p><p><strong>Set arithmetic:</strong> 92 + 45 − 7 = 130</p></div></div>
          <div className="rounded-2xl border border-slate-200 bg-white p-7"><div className="flex items-center gap-3 text-slate-700"><AlertTriangle size={22} /><h2 className="text-xl font-bold">Aug–Oct 2025 · comparison only</h2></div><p className="mt-5 leading-7 text-slate-600">1 August–31 October · 4,418 records · 1,971 short / 2,445 long / 2 balanced · 124 distinct flags.</p><div className="mt-6 grid gap-2 text-sm text-slate-600"><p><strong>Price p01/p99:</strong> −£24.95 / £157</p><p><strong>|NIV| p99:</strong> 960.5836 MWh</p><p><strong>Set arithmetic:</strong> 95 + 45 − 16 = 124</p></div></div>
        </section>
        <section className="mt-12 rounded-2xl border border-slate-200 bg-white p-7 lg:p-10"><p className="eyebrow">Why the totals differ</p><h2 className="mt-4 text-3xl font-bold text-[#102e3a]">The window moved; the percentile levels did not.</h2><p className="mt-5 max-w-4xl text-lg leading-8 text-slate-600">Both runs use price at or beyond the full-window 1st/99th percentiles and absolute NIV at or beyond its 99th percentile, with linear interpolation and inclusive ties. Q4 replaces August–September with November–December, changing both the observations and the empirical cut-offs.</p><div className="mt-9 grid gap-px overflow-hidden rounded-xl border border-slate-200 bg-slate-200 md:grid-cols-3"><Math value="+39" label="October periods newly flagged under Q4 cut-offs" /><Math value="−86" label="August–September flags removed" /><Math value="+53" label="November–December flags added" /></div><p className="mt-7 rounded-xl bg-[#102e3a] px-5 py-4 font-mono text-sm text-white">+39 − 86 + 53 = +6 · 124 + 6 = 130</p><p className="mt-6 text-sm leading-6 text-slate-500">All 31 shared October daily response hashes match, so an October data revision does not explain the discrepancy.</p></section>
        <section className="mt-12 grid gap-6 md:grid-cols-2 xl:grid-cols-4">{[
          ['Observed', 'Original Elexon source values and retained records.'],
          ['Derived', 'Deterministic calculations, classifications and reconciliations.'],
          ['Flag', 'Analytical screening or quality-control outcome.'],
          ['Hypothesis', 'Possible explanation not established by available evidence.'],
        ].map(([title, copy]) => <div key={title} className="rounded-2xl border border-slate-200 bg-white p-6"><h3 className="font-bold text-[#0d7480]">{title}</h3><p className="mt-3 leading-6 text-slate-600">{copy}</p></div>)}</section>
      </main>
    </SiteShell>
  );
}

function Math({ value, label }: { value: string; label: string }) { return <div className="bg-slate-50 p-6"><p className="text-4xl font-bold text-[#102e3a]">{value}</p><p className="mt-2 text-sm leading-6 text-slate-600">{label}</p></div>; }
