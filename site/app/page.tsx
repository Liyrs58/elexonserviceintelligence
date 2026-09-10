import Link from 'next/link';
import { ArrowRight, CheckCircle2, Database, FileCheck2, SearchCheck } from 'lucide-react';
import { SiteShell } from '@/components/site-shell';
import { metrics, workflow } from '@/lib/canonical';

export default function Home() {
  return (
    <SiteShell>
      <main>
        <section className="hero-grid border-b border-slate-200 bg-white">
          <div className="mx-auto grid max-w-[1440px] gap-14 px-5 py-20 lg:grid-cols-[1.15fr_.85fr] lg:px-10 lg:py-28">
            <div>
              <div className="inline-flex items-center gap-2 rounded-full border border-teal-200 bg-teal-50 px-3 py-1.5 text-xs font-bold uppercase tracking-[0.13em] text-[#0d7480]"><CheckCircle2 size={15} /> Canonical Q4 2025 release</div>
              <h1 className="mt-6 max-w-5xl text-balance text-5xl font-bold leading-[1.02] tracking-[-0.055em] text-[#102e3a] md:text-7xl">From settlement data to an evidence-led review queue.</h1>
              <p className="mt-7 max-w-3xl text-xl leading-8 text-slate-600">A service-analysis case study using public Elexon data, reproducible Python and SQL controls, and a four-page Power BI report definition.</p>
              <div className="mt-9 flex flex-wrap gap-3">
                <Link href="/dashboard" className="inline-flex items-center gap-2 rounded-lg bg-[#0d7480] px-5 py-3 font-semibold text-white hover:bg-[#095e68]">View dashboard pages <ArrowRight size={18} /></Link>
                <Link href="/methodology" className="inline-flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-5 py-3 font-semibold text-[#102e3a] hover:bg-slate-50">Audit the method</Link>
              </div>
            </div>
            <div className="rounded-3xl border border-slate-200 bg-[#102e3a] p-6 text-white shadow-2xl shadow-slate-300/40 md:p-8">
              <p className="text-xs font-bold uppercase tracking-[0.18em] text-teal-300">Operational question</p>
              <p className="mt-5 text-2xl font-semibold leading-9">Which Settlement Periods deserve investigation—and what can the available evidence actually establish?</p>
              <div className="mt-9 space-y-4 border-t border-white/15 pt-7">
                {[
                  ['Data gate', 'Schema, timestamps, keys and 46/48/50 coverage'],
                  ['Detection', 'Transparent full-quarter percentile screening'],
                  ['Investigation', 'Known, not established, hypothesis and next check'],
                ].map(([label, text]) => <div key={label} className="grid grid-cols-[110px_1fr] gap-4 text-sm"><span className="font-bold text-teal-300">{label}</span><span className="text-slate-200">{text}</span></div>)}
              </div>
            </div>
          </div>
        </section>

        <section className="mx-auto max-w-[1440px] px-5 py-16 lg:px-10">
          <div className="grid gap-px overflow-hidden rounded-2xl border border-slate-200 bg-slate-200 sm:grid-cols-2 xl:grid-cols-4">
            {metrics.map((metric) => <div key={metric.label} className="bg-white p-6"><p className="text-4xl font-bold tracking-[-0.04em] text-[#102e3a]">{metric.value}</p><p className="mt-2 font-semibold text-slate-700">{metric.label}</p><p className="mt-1 text-sm text-slate-500">{metric.detail}</p></div>)}
          </div>
        </section>

        <section className="border-y border-slate-200 bg-white">
          <div className="mx-auto max-w-[1440px] px-5 py-18 lg:px-10">
            <p className="eyebrow">The service-analysis pattern</p>
            <h2 className="mt-4 max-w-3xl text-4xl font-bold tracking-[-0.04em] text-[#102e3a]">The dashboard starts with trust, not a dramatic chart.</h2>
            <div className="mt-10 grid gap-4 lg:grid-cols-5">
              {workflow.map((item, index) => <div key={item} className="relative rounded-2xl border border-slate-200 bg-[#f8fafb] p-5"><span className="text-xs font-bold text-[#0d7480]">0{index + 1}</span><p className="mt-7 text-lg font-bold text-[#102e3a]">{item}</p>{index < workflow.length - 1 && <ArrowRight className="absolute -right-3 top-1/2 z-10 hidden rounded-full bg-white text-slate-400 lg:block" size={22} />}</div>)}
            </div>
          </div>
        </section>

        <section className="mx-auto grid max-w-[1440px] gap-6 px-5 py-18 md:grid-cols-3 lg:px-10">
          {[
            { icon: Database, title: 'Controlled source', copy: 'Immutable daily responses, request receipts and SHA-256 manifests preserve the retrieval trail.' },
            { icon: FileCheck2, title: 'Independent checks', copy: 'Python and DuckDB agree on nine material aggregates; 38 regression tests cover the risk points.' },
            { icon: SearchCheck, title: 'Claim discipline', copy: 'Flags are not errors. Price reconstruction is not causal attribution. Every uncertainty stays visible.' },
          ].map(({ icon: Icon, title, copy }) => <div key={title} className="rounded-2xl border border-slate-200 bg-white p-7"><Icon className="text-[#0d7480]" size={25} /><h3 className="mt-7 text-xl font-bold text-[#102e3a]">{title}</h3><p className="mt-3 leading-7 text-slate-600">{copy}</p></div>)}
        </section>
      </main>
    </SiteShell>
  );
}
