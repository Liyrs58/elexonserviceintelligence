import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';

const root=process.cwd();
const skill=process.env.PRESENTATIONS_SKILL;
const python=process.env.ARTIFACT_PYTHON;
if(!skill || !python)throw new Error('Set PRESENTATIONS_SKILL and ARTIFACT_PYTHON to the bundled runtime paths.');
const {resolvePresentationFont,applyPresentationChartFont,finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')));
const font=resolvePresentationFont({fontFamily:'DejaVu Sans'});
const tmp=path.join(root,'tmp/presentation');
await fs.mkdir(tmp,{recursive:true});
await fs.mkdir(path.join(root,'reports/presentation'),{recursive:true});
const read=async p=>JSON.parse(await fs.readFile(path.join(root,p),'utf8'));
if((await read('data/processed/run.json')).status!=='success')throw new Error('Latest pipeline run must succeed before producing the deck.');
const stats=await read('data/processed/summary.json');
const thresholds=await read('data/processed/thresholds.json');
const cases=await read('data/processed/investigations.json');
const fmt=(n,d=2)=>Number(n).toLocaleString('en-GB',{minimumFractionDigits:d,maximumFractionDigits:d});
const lengthRows=(await fs.readFile('data/processed/length_summary.csv','utf8')).trim().split('\n').slice(1).map(s=>s.split(','));
const long=lengthRows.find(r=>r[0]==='Long'),short=lengthRows.find(r=>r[0]==='Short');
// The chart is a two-decimal display snapshot; full precision stays in source CSV.
long[2]=Number(long[2]).toFixed(2);short[2]=Number(short[2]).toFixed(2);
const p=Presentation.create({slideSize:{width:1280,height:720}});
const ink='#17212B',accent='#155E75',muted='#53616B',brown='#80512B';
function text(s,value,x,y,w,h,size=26,bold=false,color=ink){
 const sh=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 sh.text=value;sh.text.style={typeface:font,fontSize:size,bold,color,autoFit:'none'};return sh;
}
function slide(title,source){
 const s=p.slides.add();s.background.fill='#FFFFFF';
 text(s,title,56,38,1168,115,36,true);
 text(s,source,140,662,1030,36,12,false,muted);
 text(s,String(p.slides.items.length),1180,662,44,28,16,false,muted);
 s.speakerNotes.textFrame.setText(source+'\nIndependent portfolio project. Not affiliated with or endorsed by Elexon. Numerical source: immutable DISEBSP snapshot retrieved 9 September 2026, Q4 2025. See SOURCES.md and METHODOLOGY.md.\nE1 https://www.elexon.co.uk/bsc/settlement/imbalance-pricing/\nE3 https://bscdocs.elexon.co.uk/guidance-notes/imbalance-pricing-guidance\nE4 https://developer.data.elexon.co.uk/api-details#api=prod-insol-insights-api');
 return s;
}
function table(s,values,x,y,w,h,widths){
 const t=s.tables.add({rows:values.length,columns:values[0].length,left:x,top:y,width:w,height:h,columnWidths:widths,values});
 t.borders.assign({fill:'#D9DFE2',width:0.6,style:'solid'});
 t.cells.block({row:0,column:0,rowCount:values.length,columnCount:values[0].length}).assign({textStyle:{fontSize:22,typeface:font,color:ink},margins:{left:14,right:14,top:10,bottom:10}});
 for(let r=0;r<values.length;r++)for(let c=0;c<values[0].length;c++){
  const cell=t.getCell(r,c);cell.fill=r===0?'#EAF0F2':'#FFFFFF';
  cell.text.style={typeface:font,fontSize:22,color:ink,bold:r===0};
 }
 return t;
}
function flow(s,labels,descriptions,y){
 const width=1168/labels.length;
 labels.forEach((label,i)=>{
  const x=56+i*width;
  text(s,label,x,y+24,width-42,72,22,true);
  text(s,descriptions[i],x,y+108,width-42,120,17,false,muted);
 });
}
let s=slide('Accurate settlement data supports disciplined investigation','Scope: Q4 2025 historical study. Domain context: Elexon imbalance pricing guidance [E1, E3].');
text(s,'GB Settlement & Imbalance Service Intelligence Monitor',56,178,1168,54,29,false,accent);
flow(s,['Elexon data','Validation','Detection','Investigation','Next action'],['Preserve the original evidence','Check coverage, values and time','Screen unusual periods','Separate known facts from hypotheses','Recommend evidence checks before escalation'],270);
text(s,'Independent portfolio project. Not affiliated with or endorsed by Elexon.',56,584,1168,42,21,false,muted);

s=slide('The workflow preserves evidence at each analytical stage','Implementation: src/ingest, src/validate, src/transform, sql/analysis.sql and powerbi/project.');
flow(s,['Official API','Immutable raw','Validated data','Semantic model','Reporting'],['Daily prices and selected price stacks','Original bytes, request receipts and SHA-256 hashes','Python controls and independent SQL summaries','Date and period dimensions\nExplicit measures','Four report pages\nStructured investigation records'],206);
text(s,'OBSERVED  Source values      DERIVED  Calculations',56,534,1168,42,27,true,accent);
text(s,'FLAG  Review rules      HYPOTHESIS  Explanations still to test',56,580,1168,42,27,true,brown);

s=slide('All 4,418 expected periods pass the core data checks','DERIVED: data/quality and summary.json. Historical completeness does not establish live service availability.');
table(s,[['Control','Snapshot result','Interpretation'],['Coverage','4,418 / 4,418','100% of expected periods'],['Duplicate keys / core nulls','0 / 0','No detected core defects'],['Schema / invalid values','0 core exceptions','Required fields pass'],['Clock change','50 periods on 26 Oct','London calendar check passes'],['Retrieval','92 / 92 daily requests','Successful snapshot retrieval']],56,176,1168,402,[370,290,508]);
text(s,'Source creation time and retrieval time remain separate. Later source revisions are possible.',56,602,1168,42,23,false,muted);

s=slide('Short-system periods had higher prices in this quarter','DERIVED: length_summary.csv; sign convention from Elexon [E1]. No causal claim.');
text(s,'Mean System Price (GBP/MWh)',56,172,760,44,26,true);
let chart=s.charts.add('bar',{position:{left:56,top:232,width:748,height:350},categories:['Long','Short'],series:[{name:'Mean price',values:[Number(long[2]),Number(short[2])],fill:accent}],barOptions:{direction:'column',grouping:'clustered'},hasLegend:false,yAxis:{min:0,max:120,majorUnit:30,numberFormatCode:'0',textStyle:{fontSize:18},majorGridlines:{fill:'#D9DFE2',width:1}},xAxis:{textStyle:{fontSize:22}},dataLabels:{showValue:true,position:'outEnd',textStyle:{fontSize:23},},chartFill:'#FFFFFF'});
applyPresentationChartFont(chart,{fontFamily:font});chart.series.getItemAt(0).valuesFormatCode='0.00';
text(s,'2,340 long periods\n2,076 short periods',860,238,360,110,28,true);
text(s,'Median prices\nLong: £62.28/MWh\nShort: £98.73/MWh',860,380,360,150,25);
text(s,'Two balanced periods sit outside this comparison.',860,554,360,78,20,false,muted);

s=slide('130 periods meet the retrospective review thresholds','FLAG: full-quarter percentiles with inclusive ties; not BSC or service limits.');
text(s,'92 price flags + 45 imbalance flags − 7 overlapping periods = 130 distinct periods',56,175,1168,70,28,true,accent);
table(s,[['Selected case','System Price','NIV','Reason'],...cases.map((c,i)=>[c.event_id,`£${fmt(c.system_price)}/MWh`,`${c.niv>0?'+':''}${fmt(c.niv)} MWh`,['Maximum price','Minimum price','Largest |NIV|'][i]])],56,280,1168,254,[360,260,260,288]);
text(s,'Price ≤ −£11.22 or ≥ £153.8997/MWh. Absolute NIV ≥ 876.0417 MWh.',56,561,1168,42,24);
text(s,'Three cases have detailed price evidence. The other 127 remain at detection level.',56,607,1168,42,23,false,muted);

s=slide('The £487 price reconciles, while the underlying cause remains open','OBSERVED + DERIVED: 13 Oct 2025 SP26 summary and offer stack [E4]. See price_reconciliation.csv.');
text(s,'KNOWN',56,188,530,46,30,true,accent);
text(s,'13 October 2025, SP26\nSystem Price: £487/MWh\nNIV: +184.92 MWh (short)\nCore quality checks pass',56,250,530,186,27);
text(s,'Retained adjusted cost / volume\n£479.6670462 / 0.9849426 MWh\n+ £0/MWh adjuster = £487/MWh',56,469,550,126,25);
text(s,'NOT ESTABLISHED',674,188,550,46,30,true,brown);
text(s,'The cause of the short position\nWhy particular actions were needed\nAny platform or service incident',674,250,550,156,27);
text(s,'The stack supports the price calculation. It does not identify the market cause. Matching prices do not prove identical source vintages.',674,445,550,166,25,false,muted);

s=slide('Further checks should test explanations before escalation','Proposed portfolio workflow, not a documented Elexon internal procedure. Price-stack checks completed for three cases.');
table(s,[['Evidence stage','Current position','Next check'],['Core data','Passed for this snapshot','Recheck revisions before reuse'],['Price calculation','Three cases reconciled','Compare calculation vintages'],['Balancing context','Partial action evidence','Inspect action timing and adjustments'],['Demand / generation','Cause still open','Test a specific supply/demand hypothesis'],['Service incident','No attribution established','Check official status and issue evidence']],56,180,1168,400,[320,330,518]);
text(s,'Escalation needs an evidence-backed issue, a clear owner and a documented next action.',56,600,1168,48,24,false,muted);

s=slide('The project makes Service Analyst work visible and reviewable','Local repository: elexon-service-intelligence/README.md. Report: powerbi/project/Settlement.pbip.');
table(s,[['Capability','Project evidence'],['Analysis','Python / SQL cross-checks and descriptive statistics'],['Validation','Executable controls, clock-change tests and source receipts'],['Investigation','130-case queue and three price reconciliations'],['Communication','Known / unknown / next-check records and insight note'],['Process improvement','Repeatable ingestion and validated rebuild workflow']],56,179,1168,362,[330,838]);
text(s,'Power BI report definitions pass structural/schema checks. Live model calculations, screenshots and interactions still require a licensed runtime.',56,568,1168,76,23,false,brown);

const candidate=path.join(tmp,'candidate.pptx');
await (await PresentationFile.exportPptx(p)).save(candidate);
for(let i=0;i<p.slides.items.length;i++){
 const blob=await p.export({slide:p.slides.items[i],format:'png',scale:1});
 await fs.writeFile(path.join(tmp,`slide-${i+1}.png`),new Uint8Array(await blob.arrayBuffer()));
}
const final=path.resolve(process.env.FINAL_PPTX??'reports/presentation/settlement-service-intelligence.pptx');
const receipt=await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath:final,pythonExecutable:python,integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit',...[3,5,7,8].flatMap(n=>['--require-native-table-slide',String(n)])],explicitTotalSlideCount:8,requiredNativeTableOwnerSlides:[3,5,7,8],requiredNativeChartOwnerSlides:[4],materializeLiteralChartWorkbooks:true,fontPolicy:{basis:'design',families:[font]},verifyArtifactToolImport:true,receiptPath:path.join(tmp,'validation.json')});
console.log(JSON.stringify({final,receipt}));
