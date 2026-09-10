import type { Metadata } from 'next';
import { PageIntro, SiteShell } from '@/components/site-shell';

export const metadata: Metadata = { title: 'Findings' };

const rows = [
  ['Mean / median System Price', '£75.7241 / £74.705 per MWh'],
  ['Highest / lowest price', '£487 / −£30 per MWh'],
  ['Largest absolute NIV', '1,563.3383 MWh'],
  ['Short / long / balanced', '2,076 / 2,340 / 2'],
  ['Pearson / Spearman', '0.6236 / 0.7631'],
];

export default function FindingsPage() {
  return (
    <SiteShell>
      <main>
        <section className="border-b border-slate-200 bg-white"><div className="mx-auto max-w-[1440px] px-5 py-16 lg:px-10 lg:py-20"><PageIntro eyebrow="Verified Q4 results" title="Useful findings, with the limits kept attached." copy="Every number on this page comes from the canonical 1 October–31 December 2025 output and has a Python/DuckDB cross-check where material." /></div></section>
        <section className="mx-auto grid max-w-[1440px] gap-8 px-5 py-16 lg:grid-cols-[.9fr_1.1fr] lg:px-10">
          <div className="rounded-2xl bg-[#102e3a] p-7 text-white lg:p-9">
            <p className="eyebrow !text-teal-300">Quarter summary</p>
            <dl className="mt-6 divide-y divide-white/15">
              {rows.map(([label, value]) => <div key={label} className="grid gap-2 py-5 sm:grid-cols-[1fr_auto] sm:items-center"><dt className="text-slate-300">{label}</dt><dd className="font-bold text-white">{value}</dd></div>)}
            </dl>
          </div>
          <div className="space-y-6">
            <div className="rounded-2xl border border-slate-200 bg-white p-7">
              <p className="eyebrow">System length comparison</p>
              <h2 className="mt-3 text-2xl font-bold text-[#102e3a]">Short periods had the higher mean price in this quarter.</h2>
              <div className="mt-8 space-y-6">
                <Bar label="Short · 2,076 periods" value="£101.2391/MWh" width="100%" tone="bg-[#0d7480]" />
                <Bar label="Long · 2,340 periods" value="£53.0677/MWh" width="52.4%" tone="bg-[#5ba6c8]" />
              </div>
              <p className="mt-7 text-sm leading-6 text-slate-500">This is a descriptive Q4 comparison. It does not establish that NIV direction caused the price difference.</p>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-white p-7">
              <p className="eyebrow">Exception population</p>
              <div className="mt-5 grid gap-4 sm:grid-cols-4">
                {[['92', 'price-tail'], ['45', 'absolute-NIV'], ['7', 'joint'], ['130', 'distinct']].map(([value, label]) => <div key={label} className="rounded-xl bg-slate-50 p-4"><p className="text-3xl font-bold text-[#102e3a]">{value}</p><p className="mt-1 text-sm text-slate-500">{label}</p></div>)}
              </div>
              <p className="mt-6 text-sm leading-6 text-slate-600">92 + 45 − 7 = 130. These are analyst review flags—not errors, incidents, forecasts or BSC limits.</p>
            </div>
          </div>
        </section>
        <section className="border-y border-slate-200 bg-white"><div className="mx-auto grid max-w-[1440px] gap-8 px-5 py-16 lg:grid-cols-[.85fr_1.15fr] lg:px-10"><div><p className="eyebrow">Selected investigation</p><h2 className="mt-4 text-4xl font-bold tracking-tight text-[#102e3a]">13 October 2025 · SP26</h2><p className="mt-5 text-lg leading-8 text-slate-600">The quarter&apos;s highest observed price was £487/MWh with NIV +184.9225 MWh, a short system.</p></div><div className="grid gap-4 sm:grid-cols-2"><EvidenceCard label="Established" copy="Core controls passed. Retained offer rows, volume and adjuster reconstruct £487/MWh to penny precision." /><EvidenceCard label="Not established" copy="Why the actions were accepted, what caused the system condition, or whether a service incident occurred." /><EvidenceCard label="Hypothesis" copy="Remaining balancing-action prices may explain price severity better than NIV magnitude alone." /><EvidenceCard label="Next check" copy="Align source vintages, then inspect targeted balancing actions and demand/generation evidence." /></div></div></section>
      </main>
    </SiteShell>
  );
}

function Bar({ label, value, width, tone }: { label: string; value: string; width: string; tone: string }) {
  return <div><div className="mb-2 flex justify-between gap-3 text-sm"><span className="font-semibold text-slate-700">{label}</span><span className="font-bold text-[#102e3a]">{value}</span></div><div className="h-3 rounded-full bg-slate-100"><div className={`h-3 rounded-full ${tone}`} style={{ width }} /></div></div>;
}

function EvidenceCard({ label, copy }: { label: string; copy: string }) {
  return <div className="rounded-2xl border border-slate-200 bg-[#f8fafb] p-5"><p className="text-xs font-bold uppercase tracking-[0.14em] text-[#0d7480]">{label}</p><p className="mt-3 leading-7 text-slate-600">{copy}</p></div>;
}
