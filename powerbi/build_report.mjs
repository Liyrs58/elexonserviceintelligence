import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const report='powerbi/project/Settlement.Report';
const schema='https://developer.microsoft.com/json-schemas/fabric/item/report/definition/';
const id=s=>crypto.createHash('sha256').update(s).digest('hex').slice(0,20);
const save=(p,o)=>{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,JSON.stringify(o,null,2)+'\n');};
save(report+'/.platform',{$schema:'https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json',metadata:{type:'Report',displayName:'GB Settlement & Imbalance Service Intelligence Monitor'},config:{version:'2.0',logicalId:'6b82e314-2fea-4ef1-b767-057d375018df'}});
const lit=v=>({expr:{Literal:{Value:typeof v==='boolean'?String(v):typeof v==='number'?v+'D':"'"+v.replaceAll("'","''")+"'"}}});
const fill=v=>({solid:{color:lit(v)}});
const obj=properties=>[{properties}];
const col=(t,p)=>({Column:{Expression:{SourceRef:{Entity:t}},Property:p}});
const measure=(t,p)=>({Measure:{Expression:{SourceRef:{Entity:t}},Property:p}});
const C=(t,p)=>({field:col(t,p),queryRef:t+'.'+p,nativeQueryRef:p});
const M=(t,p)=>({field:measure(t,p),queryRef:t+'.'+p,nativeQueryRef:p});
const price='#155E75',niv='#80512B',ink='#17212B';
const pages=[];
function page(title,archetype,variant,rationale){
 const p={name:id(title),title,archetype,variant,rationale,items:[]};pages.push(p);return p;
}
function add(p,key,type,title,rect,roles={},options={}){p.items.push({key,type,title,rect,roles,...options});}
function text(p,key,value,rect,size=20){add(p,key,'textbox',value,rect,{}, {size});}
function slice(p,key,t,c,rect,single=false){add(p,key,'slicer',c,rect,{Values:[C(t,c)]},{single});}
function chart(p,key,type,title,rect,category,values,color=price){add(p,key,type,title,rect,{Category:[category],Y:values},{color,sort:category});}
function table(p,key,title,rect,fields){add(p,key,'tableEx',title,rect,{Values:fields});}
function cards(p,key,rect,fields){add(p,key,'cardVisual','',rect,{Data:fields});}
function header(p){text(p,'page_title',p.title,[32,24,1120,56],28);text(p,'scope','Q4 2025 | Historical snapshot | Independent portfolio project',[32,88,1120,32],14);}
const p1=page('Settlement Service Monitor','Operational','A','Desk-based review combines data status, aligned time views and a visible exception queue.');header(p1);
slice(p1,'dates','Date','Date',[1448,24,440,88]);
cards(p1,'status',[32,144,1856,160],[M('Settlement','Settlement Periods'),M('Daily Controls','Data Completeness %'),M('Settlement','Analytical Exceptions'),M('Daily Controls','Validation Exceptions')]);
chart(p1,'prices','lineChart','Daily average System Price | GBP/MWh',[32,328,1040,320],C('Date','Date'),[M('Settlement','Average System Price')]);
chart(p1,'niv','lineChart','Daily average signed NIV | MWh',[32,672,1040,320],C('Date','Date'),[M('Settlement','Average NIV')],niv);
add(p1,'queue','tableEx','Analytical exception queue | select a period for context',[1096,328,792,664],{Values:[C('Settlement','Event'),C('Settlement','System Length'),C('Settlement','System Price Value'),C('Settlement','NIV Value'),C('Settlement','Reason'),C('Settlement','Severity'),C('Settlement','Quality Status')]},{exceptionOnly:true,sort:C('Settlement','System Price Value'),descending:true});
text(p1,'note','Data through 31 Dec 2025. Full-quarter thresholds remain fixed when filtering. Analytical flags are not service incidents.',[32,1016,1856,40],14);
const p2=page('Market & Settlement Analysis','Analytical','B','Two useful slicers and six analytical views use the full canvas width.');header(p2);
slice(p2,'month','Date','Month',[1200,24,320,88]);slice(p2,'length','Settlement','System Length',[1544,24,344,88]);
add(p2,'compare','pivotTable','Short / long comparison | GBP/MWh',[32,144,584,376],{Rows:[C('Settlement','System Length')],Values:[M('Settlement','Settlement Periods'),M('Settlement','Average System Price'),M('Settlement','Median System Price')]});
chart(p2,'distribution','columnChart','Price distribution | 20 GBP/MWh bins',[640,144,600,376],C('Settlement','Price Bin'),[M('Settlement','Settlement Periods')]);
chart(p2,'intraday','lineChart','Average price by period index | GBP/MWh',[1264,144,624,376],C('Settlement Period','Period'),[M('Settlement','Average System Price')]);
chart(p2,'nivdistribution','columnChart','NIV distribution | 100 MWh bins',[32,544,584,448],C('Settlement','NIV Bin'),[M('Settlement','Settlement Periods')],niv);
add(p2,'relationship','scatterChart','NIV versus System Price | MWh × GBP/MWh',[640,544,824,448],{Category:[C('Settlement','Event')],X:[M('Settlement','Average NIV')],Y:[M('Settlement','Average System Price')]},{color:price});
cards(p2,'tails',[1488,544,400,192],[M('Settlement','Extreme Price Periods'),M('Settlement','Extreme Imbalance Periods')]);
text(p2,'interpretation','DESCRIPTIVE ASSOCIATION\nNIV direction and price are related in this quarter. Their association does not establish causality. SP49/50 occur only on the autumn clock-change day.',[1488,760,400,232],17);
text(p2,'note','OBSERVED price and NIV; DERIVED summaries. Histograms show bin lower bounds. Review sample counts before comparing period indices.',[32,1016,1856,40],14);
const p3=page('Exception Investigation','Narrative','A','Single-event selection separates established evidence from untested explanations in two columns.');header(p3);
slice(p3,'event','Investigation','Event',[1360,24,528,88],true);
table(p3,'eventdetail','EVENT / WHAT HAPPENED',[32,144,904,184],[C('Investigation','Event'),C('Investigation','What Happened')]);
table(p3,'flagdetail','WHY FLAGGED / DATA QUALITY',[960,144,928,184],[C('Investigation','Why Flagged'),C('Investigation','Data Quality')]);
table(p3,'known','KNOWN | observed and reconciled evidence',[32,352,904,368],[C('Investigation','Known')]);
table(p3,'unknown','NOT ESTABLISHED',[960,352,928,184],[C('Investigation','Not Established')]);
table(p3,'hypotheses','HYPOTHESES | unconfirmed',[960,560,928,160],[C('Investigation','Hypotheses')]);
table(p3,'next','RECOMMENDED NEXT CHECKS',[32,744,1200,248],[C('Investigation','Next Checks')]);
table(p3,'state','INVESTIGATION STATUS',[1256,744,632,248],[C('Investigation','Investigation Status')]);
text(p3,'note','130 flagged periods are selectable. Only three have detailed price-stack evidence. Other cases remain queued for investigation.',[32,1016,1856,40],14);
const p4=page('Data Quality & Controls','Operational','C','Audit table dominates; daily key coverage and whole-snapshot retrieval checks stay distinct.');header(p4);
slice(p4,'dates','Date','Date',[1448,24,440,88]);
cards(p4,'quality',[32,144,1856,160],[M('Date','Expected Settlement Periods'),M('Settlement','Settlement Periods'),M('Daily Controls','Data Completeness %'),M('Daily Controls','Missing Settlement Periods'),M('Daily Controls','Duplicate Settlement Periods'),M('Daily Controls','Null Values')]);
table(p4,'source','Whole-snapshot source and retrieval controls',[32,328,1856,360],[C('Source Controls','Control'),C('Source Controls','Status'),C('Source Controls','Detail')]);
add(p4,'daily','pivotTable','Daily coverage | clock changes included in expected counts',[32,712,1168,280],{Rows:[C('Date','Date')],Values:[M('Date','Expected Settlement Periods'),M('Settlement','Settlement Periods'),M('Daily Controls','Data Completeness %'),M('Daily Controls','Validation Exceptions')]});
text(p4,'clock','CLOCK-CHANGE CONTROL\n26 October contains 50 periods. Expected coverage is calculated from London midnights in UTC.\n\nThis historical snapshot does not measure present service availability.',[1224,712,664,280],18);
text(p4,'note','Retrieval: 9 September 2026 UTC. Required fields validated before analysis. Source controls apply to the full snapshot, regardless of slicers.',[32,1016,1856,40],14);
// Persist concrete geometry before authoring. JSON is also valid YAML 1.2.
const brief={generated_by:'powerbi-report-design',contract_version:1,mode:'greenfield',design_identity:{tone:'Restrained operational analysis',signature:'Source/status band and explicit evidence labels'},color_map:{'System Price':price,NIV:niv},pages:pages.map(p=>({name:p.title,archetype:p.archetype,layout_variant:p.variant,variant_rationale:p.rationale,layout_contract:{canvas:{width:1920,height:1080,margin:32,gutter:24,snap:8},placements:p.items.map(i=>({id:i.key,kind:i.type,text:i.title,position:i.rect,field_bindings:i.roles,purpose:i.title})),space_audit:{unplaced_regions:[],balance_rationale:p.rationale}}})),accessibility:{font:'Segoe UI',minimum_font_pt:14,status:'Text labels supplement colour; runtime inspection pending'},overrides:'No gradients, smoothing, gauges or decorative cards. Page3 event slicer is explicitly required by user despite narrative archetype defaults.'};
save('powerbi/design-brief.json',brief);
save('powerbi/project/Settlement.pbip',{$schema:'https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json',version:'1.0',artifacts:[{report:{path:'Settlement.Report'}}],settings:{enableAutoRecovery:true}});
save(report+'/definition.pbir',{$schema:'https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json',version:'4.0',datasetReference:{byPath:{path:'../Settlement.SemanticModel'}}});
save(report+'/definition/version.json',{$schema:schema+'versionMetadata/1.0.0/schema.json',version:'2.0.0'});
save(report+'/definition/report.json',{$schema:schema+'report/3.3.0/schema.json',themeCollection:{}});
save(report+'/definition/pages/pages.json',{$schema:schema+'pagesMetadata/1.0.0/schema.json',pageOrder:pages.map(p=>p.name),activePageName:p1.name});
function chrome(title){return {background:obj({show:lit(true),color:fill('#FFFFFF'),transparency:lit(0)}),border:obj({show:lit(false),radius:lit(0)}),padding:obj({top:lit(8),bottom:lit(8),left:lit(8),right:lit(8)}),visualHeader:obj({show:lit(false)}),title:obj({show:lit(Boolean(title)),text:lit(title),fontSize:lit(16),fontColor:fill(ink),titleWrap:lit(true)})};}
for(const p of pages){
 const base=report+'/definition/pages/'+p.name;
 save(base+'/page.json',{$schema:schema+'page/2.1.0/schema.json',name:p.name,displayName:p.title,displayOption:'FitToPage',height:1080,width:1920,objects:{background:obj({color:fill('#F3F4F4'),transparency:lit(0)})}});
 for(const [index,i] of p.items.entries()){
  const [x,y,width,height]=i.rect;
  const v={$schema:schema+'visualContainer/2.9.0/schema.json',name:id(p.name+i.key),position:{x,y,width,height,z:index*1000,tabOrder:index},visual:{visualType:i.type,visualContainerObjects:chrome(i.title)}};
  const visual=v.visual;
  if(i.type==='textbox'){
   visual.objects={general:obj({paragraphs:i.title.split('\n').map(value=>({textRuns:[{value,textStyle:{fontFamily:'Segoe UI',fontSize:i.size+'pt',color:ink}}],horizontalTextAlignment:'left'}))})};
   visual.visualContainerObjects=chrome('');visual.visualContainerObjects.background=obj({show:lit(false)});visual.visualContainerObjects.padding=obj({top:lit(0),bottom:lit(0),left:lit(0),right:lit(0)});
  } else {
   visual.query={queryState:Object.fromEntries(Object.entries(i.roles).map(([role,projections])=>[role,{projections}]))};
   visual.objects={};
   if(i.sort)visual.query.sortDefinition={sort:[{field:i.sort.field,direction:i.descending?'Descending':'Ascending'}],isDefaultSort:false};
   if(i.type==='slicer'){
    visual.visualContainerObjects.title=obj({show:lit(false)});
    visual.objects={data:obj({mode:lit('Dropdown')}),header:obj({show:lit(true),text:lit(i.title),textSize:lit(14)}),selection:obj({strictSingleSelect:lit(Boolean(i.single))})};
   }
   if(i.type==='tableEx'||i.type==='pivotTable'){
    visual.objects.columnHeaders=obj({autoSizeColumnWidth:lit(true),columnAdjustment:lit('growToFit'),fontSize:lit(14),wordWrap:lit(true)});
    visual.objects.values=obj({fontSize:lit(14),wordWrap:lit(true),fontColorPrimary:fill(ink),fontColorSecondary:fill(ink),backColorPrimary:fill('#FFFFFF'),backColorSecondary:fill('#F5F6F6')});
    visual.visualContainerObjects.stylePreset=obj({name:lit('None')});
   }
   if(i.type==='cardVisual'){
    // h160: 16 VCO +48 default inner allowance +42 value +18 label+2 spacing=126.
    visual.objects.value=[{properties:{fontSize:lit(28),fontColor:fill(ink)},selector:{id:'default'}}];
    visual.objects.layout=[{properties:{paddingUniform:{expr:{Literal:{Value:'0L'}}},style:lit('Table')},selector:{id:'default'}}];
    visual.objects.outline=[{properties:{show:lit(false)},selector:{id:'default'}}];
   }
   if(i.color)visual.objects.dataPoint=obj({defaultColor:fill(i.color)});
   if(i.type==='lineChart')visual.objects.lineStyles=obj({lineChartType:lit('linear'),areaShow:lit(false),showMarker:lit(false),strokeWidth:lit(2)});
  }
  if(i.exceptionOnly){
   const condition={In:{Expressions:[{Column:{Expression:{SourceRef:{Source:'s'}},Property:'Exception'}}],Values:[[{Literal:{Value:'true'}}]]}};
   v.filterConfig={filters:[{name:'Filter'+id(p.name+i.key+'filter')+'0000',field:col('Settlement','Exception'),type:'Categorical',howCreated:'User',filter:{Version:2,From:[{Name:'s',Entity:'Settlement',Type:0}],Where:[{Condition:condition}]}}]};
  }
  save(base+'/visuals/'+v.name+'/visual.json',v);
 }
}
console.log(`Built ${pages.length} pages, ${pages.reduce((n,p)=>n+p.items.length,0)} visuals. Offline validation and live review required.`);
