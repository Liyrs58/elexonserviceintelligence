import type { Metadata } from 'next';
import { PageIntro, SiteShell } from '@/components/site-shell';

export const metadata: Metadata = { title: 'Candidate view' };

const capabilities = [
  ['Analytical investigation', 'A 130-period review queue with three evidence-led deep dives and explicit next checks.'],
  ['Data quality', 'Schema, timestamp, duplicate, coverage, clock-change, hash and stale-run controls.'],
  ['SQL and Python', 'Independent DuckDB aggregation and a reproducible Python pipeline with 38 passing tests.'],
  ['Power BI', 'Six-table semantic model, 19 measures, four pages and 39 data-bound visual definitions.'],
  ['Stakeholder communication', 'One-page service note, eight-slide presentation and known-versus-unknown framing.'],
  ['Learning ownership', 'Applied official Elexon/BSC guidance to a new domain while preserving evidence boundaries.'],
];

export default function InterviewPage() {
  return (
    <SiteShell>
      <main>
        <section className="border-b border-slate-200 bg-white"><div className="mx-auto max-w-[1440px] px-5 py-16 lg:px-10 lg:py-20"><PageIntro eyebrow="Recruiter and interviewer view" title="What this project demonstrates—and what it does not." copy="A concise map from the work completed to Service Analyst capabilities, with the Power BI runtime boundary stated plainly." /></div></section>
        <section className="mx-auto max-w-[1440px] px-5 py-16 lg:px-10">
          <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">{capabilities.map(([title, copy], index) => <article key={title} className="rounded-2xl border border-slate-200 bg-white p-6"><span className="text-xs font-bold text-[#0d7480]">0{index + 1}</span><h2 className="mt-6 text-xl font-bold text-[#102e3a]">{title}</h2><p className="mt-3 leading-7 text-slate-600">{copy}</p></article>)}</div>
        </section>
        <section className="border-y border-slate-200 bg-white"><div className="mx-auto grid max-w-[1440px] gap-10 px-5 py-16 lg:grid-cols-2 lg:px-10"><div><p className="eyebrow">30-second explanation</p><blockquote className="mt-5 border-l-4 border-[#0d7480] pl-6 text-xl leading-9 text-[#102e3a]">I built an independent service-intelligence project using public Elexon Settlement Period data. I validated all 4,418 expected Q4 2025 periods with Python and SQL, including the 50-period clock-change day, then created an explainable review queue for 130 unusual price or NIV periods. The Power BI definition moves from controls to investigation while keeping facts, calculations and unproven explanations separate.</blockquote></div><div className="rounded-2xl bg-[#102e3a] p-7 text-white"><p className="text-xs font-bold uppercase tracking-[0.14em] text-teal-300">Honest limitation</p><h2 className="mt-4 text-2xl font-bold">Structurally validated, not runtime-verified.</h2><p className="mt-4 leading-7 text-slate-200">Official Microsoft tooling parses the report definition and semantic model. Live M refresh, DAX execution, filters, accessibility and performance need licensed Power BI Desktop or Fabric. The downloadable Windows reviewer bundle contains the exact close-out checklist.</p></div></div></section>
        <section className="mx-auto max-w-[1440px] px-5 py-16 lg:px-10"><p className="eyebrow">Evidence-safe CV wording</p><div className="mt-6 grid gap-5 lg:grid-cols-2"><div className="rounded-2xl border border-slate-200 bg-white p-7"><p className="leading-8 text-slate-700">Validated 4,418 public Elexon Insights Settlement Period records across Q4 2025 using Python and SQL, implementing completeness, schema, timestamp, duplicate and 46/48/50 clock-change controls.</p></div><div className="rounded-2xl border border-slate-200 bg-white p-7"><p className="leading-8 text-slate-700">Built a four-page Power BI service-monitoring and investigation report with a six-table semantic model, screening 130 unusual System Price/NIV periods and reconciling three selected price cases against official balancing evidence while separating observed findings from unestablished causes.</p></div></div></section>
      </main>
    </SiteShell>
  );
}
