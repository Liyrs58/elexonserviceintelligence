// Deterministic local PBIP model generation. Runtime DAX verification is separate.
import fs from 'node:fs';
import path from 'node:path';
const root=path.resolve('.');
const target=path.join(root,'powerbi/project/Settlement.SemanticModel');
const def=path.join(target,'definition');
fs.mkdirSync(path.join(def,'tables'),{recursive:true});
const json=(p,o)=>fs.writeFileSync(p,JSON.stringify(o,null,2)+'\n');
const quote=s=>`'${s.replaceAll("'","''")}'`;
json(path.join(target,'definition.pbism'),{$schema:'https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json',version:'4.2',settings:{qnaEnabled:true}});
fs.writeFileSync(path.join(def,'database.tmdl'),'database Settlement\n\tcompatibilityLevel: 1702\n\tcompatibilityMode: powerBI\n');
const tables=[];
const relationships=[];
const catalog=[];
function table(name,file,columns,measures=[],description=''){
  tables.push(name);
  let text=`/// ${description}\ntable ${quote(name)}\n`;
  if(name==='Date')text+='\tdataCategory: Time\n';
  for(const [title,dax,format,explanation] of measures){
    text+=`\n\t/// DERIVED: ${explanation}\n\tmeasure ${quote(title)} = ${dax}\n\t\tformatString: ${format}\n\t\tdisplayFolder: Monitor\n\t\tannotation EvidenceClass = DERIVED\n`;
    catalog.push({table:name,measure:title,dax,format,definition:explanation,runtime_status:'Not executed: licensed Power BI/Analysis Services environment required'});
  }
  for(const [title,source,type,hidden=false,evidence='OBSERVED',description=title] of columns){
    text+=`\n\t/// ${evidence}: ${description}\n\tcolumn ${quote(title)}\n\t\tdataType: ${type}\n${hidden?'\t\tisHidden\n':''}\t\tsummarizeBy: none\n\t\tsourceColumn: ${source}\n\t\tannotation EvidenceClass = ${evidence}\n`;
    if(type==='dateTime')text+='\t\tformatString: yyyy-MM-dd\n';
    if(name==='Date' && title==='Month')text+="\t\tsortByColumn: 'Month Number'\n";
  }
  const types={string:'type text',int64:'Int64.Type',double:'type number',decimal:'Currency.Type',boolean:'type logical',dateTime:'type date'};
  const conversions=columns.map(c=>`{"${c[1]}", ${types[c[2]]}}`).join(', ');
  text+=`\n\tpartition ${quote(name)} = m\n\t\tmode: import\n\t\tsource =\n\t\t\tlet\n\t\t\t\tSource = Csv.Document(File.Contents(DataFolder & "/${file}"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),\n\t\t\t\tHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),\n\t\t\t\tTyped = Table.TransformColumnTypes(Headers, {${conversions}}, "en-GB")\n\t\t\tin\n\t\t\t\tTyped\n`;
  // Force every CSV query to evaluate the latest pipeline status before reading.
  text=text.replace('Source = Csv.Document(', 'Run = Json.Document(File.Contents(DataFolder & "/processed/run.json")),\n\t\t\t\tSource = if Record.FieldOrDefault(Run, "status", "unknown") <> "success" then error "Latest pipeline run did not succeed. Rebuild validated outputs before refreshing." else Csv.Document(');
  fs.writeFileSync(path.join(def,'tables',name+'.tmdl'),text);
}
const price='#,##0.00 "GBP/MWh"',volume='#,##0.00 "MWh"',count='#,##0';
table('Date','processed/dates.csv',[
 ['Date','settlement_date','dateTime',false,'DERIVED','Contiguous local Settlement Day calendar'],
 ['Expected Periods','expected_periods','int64',true,'DERIVED','UTC elapsed time between London midnights / 30 minutes'],
 ['Year','year','int64'],['Month Number','month','int64'],['Month','month_name','string'],['Weekday','weekday','string'],['Clock Change','clock_change','boolean',false,'DERIVED']
],[['Expected Settlement Periods',"SUM('Date'[Expected Periods])",count,'Expected half-hours under selected dates, including clock changes']], 'Date dimension, one row per Settlement Day');
table('Settlement Period','processed/periods.csv',[
 ['Period','settlement_period','int64',false,'DERIVED','Period index 1 to 50; index is not a universal local-clock label']
],[],'Settlement Period index dimension');
table('Settlement','processed/settlement.csv',[
 ['Date','settlement_date','dateTime',true],['Period','settlement_period','int64',true],['Event','event_id','string',false,'DERIVED'],
 ['System Price Value','system_price','double',true,'DERIVED','GBP/MWh; source buy price after buy/sell equality check'],
 ['NIV Value','niv','double',true,'OBSERVED','Net Imbalance Volume in MWh'],
 ['Absolute NIV Value','absolute_niv','double',true,'DERIVED','Absolute Net Imbalance Volume in MWh'],
 ['System Length','system_length','string',false,'DERIVED','Positive NIV Short, negative Long, zero Balanced'],
 ['Price Percentile','price_percentile','double',false,'DERIVED','Full-quarter empirical upper rank, 0–100'],
 ['NIV Percentile','niv_percentile','double',false,'DERIVED','Full-quarter absolute-NIV upper rank, 0–100'],
 ['Price Flag','price_flag','boolean',true,'FLAG'],['Imbalance Flag','imbalance_flag','boolean',true,'FLAG'],
 ['Exception','is_exception','boolean',false,'FLAG'],['Reason','reason_flagged','string',false,'FLAG'],
 ['Severity','severity','string',false,'FLAG','Analytical review priority, not operational incident severity'],
 ['Quality Status','quality_status','string',false,'FLAG'],
 ['Price Bin','price_bin_lower','int64',false,'DERIVED','Lower edge of 20 GBP/MWh bin'],
 ['NIV Bin','niv_bin_lower','int64',false,'DERIVED','Lower edge of 100 MWh bin'],
 ['Retrieval UTC','retrieved_at','string',false,'OBSERVED']
],[
 ['Settlement Periods',"COUNTROWS('Settlement')",count,'Received period count within filter context'],
 ['Average System Price',"AVERAGE('Settlement'[System Price Value])",price,'Arithmetic mean of period prices'],
 ['Median System Price',"MEDIAN('Settlement'[System Price Value])",price,'Median of period prices'],
 ['Maximum System Price',"MAX('Settlement'[System Price Value])",price,'Highest period price'],
 ['Minimum System Price',"MIN('Settlement'[System Price Value])",price,'Lowest period price'],
 ['Average NIV',"AVERAGE('Settlement'[NIV Value])",volume,'Mean signed NIV'],
 ['Average Absolute NIV',"AVERAGE('Settlement'[Absolute NIV Value])",volume,'Mean absolute NIV'],
 ['Maximum Absolute NIV',"MAX('Settlement'[Absolute NIV Value])",volume,'Largest absolute NIV'],
 ['Short Settlement Periods',"CALCULATE([Settlement Periods], KEEPFILTERS('Settlement'[System Length] = \"Short\"))",count,'Count of positive-NIV periods'],
 ['Long Settlement Periods',"CALCULATE([Settlement Periods], KEEPFILTERS('Settlement'[System Length] = \"Long\"))",count,'Count of negative-NIV periods'],
 ['Extreme Price Periods',"CALCULATE([Settlement Periods], KEEPFILTERS('Settlement'[Price Flag] = TRUE()))",count,'Period count satisfying fixed full-quarter price thresholds'],
 ['Extreme Imbalance Periods',"CALCULATE([Settlement Periods], KEEPFILTERS('Settlement'[Imbalance Flag] = TRUE()))",count,'Period count satisfying fixed full-quarter absolute-NIV threshold'],
 ['Analytical Exceptions',"CALCULATE([Settlement Periods], KEEPFILTERS('Settlement'[Exception] = TRUE()))",count,'Distinct periods flagged by either screening rule']
], 'One validated observation per Settlement Date and Period; latest DISEBSP snapshot');
table('Daily Controls','quality/daily_controls.csv',[
 ['Date','settlement_date','dateTime',true,'DERIVED'],['Expected','expected_periods','int64',true,'DERIVED'],
 ['Received','received_periods','int64',true,'DERIVED'],['Missing','missing_periods','int64',true,'FLAG'],
 ['Duplicates','duplicate_periods','int64',true,'FLAG'],['Nulls','null_values','int64',true,'FLAG'],
 ['Schema Exceptions','schema_exceptions','int64',true,'FLAG'],['Exceptions','validation_exceptions','int64',true,'FLAG'],
 ['Retrieval Status','retrieval_status','string',false,'OBSERVED'],['Clock Change','clock_change','boolean',false,'DERIVED']
],[
 ['Data Completeness %',"DIVIDE(SUM('Daily Controls'[Received]), SUM('Daily Controls'[Expected]))",'0.00%','Key coverage for selected dates; unaffected by market-length or price filters'],
 ['Missing Settlement Periods',"SUM('Daily Controls'[Missing])",count,'Absent expected date-period keys'],
 ['Duplicate Settlement Periods',"SUM('Daily Controls'[Duplicates])",count,'Duplicate date-period keys'],
 ['Validation Exceptions',"SUM('Daily Controls'[Exceptions])",count,'Core validation events'],
 ['Null Values',"SUM('Daily Controls'[Nulls])",count,'Required core null values']
], 'Daily control fact; one row per Settlement Day. Market filters intentionally do not affect denominator');
table('Source Controls','quality/source_controls.csv',[
 ['Control','control','string',false,'DERIVED'],['Status','status','string',false,'FLAG'],['Detail','detail','string',false,'DERIVED']
],[],'Disconnected audit utility table, whole-snapshot controls unaffected by analytical slicers');
// Every flagged period is selectable, with reviewed evidence only for the three cases.
// CSV input remains generated by the Python pipeline. Expanded investigations is generated separately.
table('Investigation','processed/investigation_queue.csv',[
 ['Date','settlement_date','dateTime',true],['Event','event_id','string',false,'DERIVED'],
 ['What Happened','what_happened','string',false,'DERIVED'],['Why Flagged','reason_flagged','string',false,'FLAG'],
 ['Data Quality','quality_control_result','string',false,'FLAG'],['Known','known','string',false,'DERIVED'],
 ['Not Established','not_established','string',false,'HYPOTHESIS'],['Hypotheses','hypotheses','string',false,'HYPOTHESIS'],
 ['Next Checks','recommended_next_checks','string',false,'DERIVED'],['Investigation Status','investigation_status','string',false,'DERIVED']
],[],'One record per flagged period. Three reviewed cases contain retrieved price-stack evidence');
for(const name of ['Settlement','Daily Controls','Investigation'])relationships.push(`relationship ${quote(name+' to Date')}\n\tfromColumn: ${quote(name)}.Date\n\ttoColumn: 'Date'.Date\n\tcrossFilteringBehavior: oneDirection\n`);
relationships.push("relationship 'Settlement to Period'\n\tfromColumn: 'Settlement'.Period\n\ttoColumn: 'Settlement Period'.Period\n\tcrossFilteringBehavior: oneDirection\n");
fs.writeFileSync(path.join(def,'relationships.tmdl'),relationships.join('\n'));
fs.writeFileSync(path.join(def,'expressions.tmdl'),`/// Root data folder. Change this single parameter when moving the project.\nexpression DataFolder = "${path.join(root,'data').replaceAll('"','""')}" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]\n`);
fs.writeFileSync(path.join(def,'model.tmdl'),`model Model\n\tculture: en-GB\n\tdefaultPowerBIDataSourceVersion: powerBI_V3\n\tsourceQueryCulture: en-GB\n\tdiscourageImplicitMeasures\n\n${tables.map(n=>'ref table '+quote(n)).join('\n')}\n`);
json('powerbi/measure-catalog.json',catalog);
console.log(`Created ${tables.length} tables, ${relationships.length} relationships, ${catalog.length} explicit measures. Runtime verification pending.`);
