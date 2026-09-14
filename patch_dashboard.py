from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
if 'dashboard-visual-grid' in s:
    print('Dashboard patch already applied')
    raise SystemExit(0)
css=r'''<style>
#view-overview{--dash-glow:rgba(139,108,249,.16)}
#view-overview .kpi-row{gap:12px}#view-overview .kpi{min-height:78px;transition:transform .2s ease,border-color .2s ease,box-shadow .2s ease;background:linear-gradient(145deg,rgba(23,30,56,.98),rgba(16,21,40,.98))}#view-overview .kpi:hover{transform:translateY(-3px);border-color:var(--accent);box-shadow:0 12px 32px rgba(0,0,0,.22)}#view-overview .kpi .value{animation:kpiPop .45s ease both}@keyframes kpiPop{from{opacity:0;transform:translateY(8px) scale(.97)}to{opacity:1;transform:none}}
.dashboard-visual-grid{display:grid;grid-template-columns:1.05fr 1.25fr 1.05fr;gap:14px;margin-top:14px}.dashboard-visual-grid .panel{min-width:0;position:relative;overflow:hidden}.dashboard-visual-grid .panel:after{content:'';position:absolute;inset:auto -35px -55px auto;width:120px;height:120px;background:radial-gradient(circle,var(--dash-glow),transparent 70%);pointer-events:none}.dashboard-visual-grid h3{display:flex;justify-content:space-between;align-items:center;gap:8px}.dashboard-visual-grid h3 span{font-size:10px;font-weight:500;color:var(--muted)}.donut-wrap{height:215px;position:relative;display:flex;align-items:center;justify-content:center}.donut-wrap canvas{max-height:205px}.chart-center{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;flex-direction:column;pointer-events:none;line-height:1.15}.chart-center b{font-size:18px}.chart-center small{font-size:9px;color:var(--muted);margin-top:4px}.video-bar-wrap{height:215px;position:relative}.interactive-hint{font-size:9px;color:var(--muted);opacity:.85}.dashboard-table-panel{margin-top:14px}.dashboard-table-panel tbody tr{cursor:pointer;transition:background .15s ease,transform .15s ease}.dashboard-table-panel tbody tr:hover{background:rgba(139,108,249,.09)}.dashboard-table-panel tbody tr.is-focus{background:rgba(47,214,196,.10);box-shadow:inset 3px 0 0 var(--teal)}.mini-share{display:inline-flex;align-items:center;gap:6px;padding:4px 8px;border-radius:999px;background:#0e1424;border:1px solid var(--border);font-size:10px;color:var(--muted)}.mini-share i{width:6px;height:6px;border-radius:50%;background:var(--teal);display:block}@media(max-width:980px){.dashboard-visual-grid{grid-template-columns:1fr 1fr}.dashboard-visual-grid .panel:nth-child(2){grid-column:1/-1}}@media(max-width:680px){.dashboard-visual-grid{grid-template-columns:1fr}.dashboard-visual-grid .panel:nth-child(2){grid-column:auto}.donut-wrap,.video-bar-wrap{height:230px}}
</style>'''
s=s.replace('</head>',css+'</head>',1)
start=s.index('      <div class="view active" id="view-overview">')
end=s.index('\n      <!-- ===== الفروع ===== -->',start)
new=r'''      <div class="view active" id="view-overview">
        <div class="kpi-row">
          <div class="kpi" style="--accent:#8b6cf9"><div class="label">إجمالي المبيعات</div><div class="value mono" id="kpiTotalSales">—</div></div>
          <div class="kpi" style="--accent:#2fd6c4"><div class="label">أفضل فرع مبيعاً</div><div class="value" id="kpiBestBranch" style="font-size:15px;">—</div></div>
          <div class="kpi" style="--accent:#f0a63a"><div class="label">أكثر صنف حركة</div><div class="value" id="kpiTopProduct" style="font-size:14px;">—</div></div>
          <div class="kpi" style="--accent:#e8479f"><div class="label">عدد التقارير</div><div class="value mono" id="kpiDeadCount">—</div></div>
        </div>
        <div class="dashboard-visual-grid">
          <div class="panel"><h3>توزيع المبيعات <span class="interactive-hint">اضغط على الجزء لتحديد الفرع</span></h3><div class="donut-wrap"><canvas id="chartSalesShare"></canvas><div class="chart-center"><b id="salesShareCenter">—</b><small>إجمالي المبيعات</small></div></div></div>
          <div class="panel"><h3>أعلى الفروع مبيعاً <span>مقارنة تفاعلية</span></h3><div class="video-bar-wrap"><canvas id="chartTopBranches"></canvas></div></div>
          <div class="panel"><h3>توزيع التقارير <span class="interactive-hint">حسب الفروع</span></h3><div class="donut-wrap"><canvas id="chartReportsShare"></canvas><div class="chart-center"><b id="reportsShareCenter">—</b><small>تقرير مرفوع</small></div></div></div>
        </div>
        <div class="panel dashboard-table-panel"><h3>تفاصيل ومقارنة الفروع <span id="branchTableCount"></span></h3><div class="controls"><input type="text" class="search-box" id="branchSearch" placeholder="ابحث عن فرع..."><span class="mini-share"><i></i> اضغط على أي صف لفتح تفاصيل الفرع</span></div><div class="preview-scroll" style="max-height:420px;"><table><thead><tr><th>الفرع</th><th>عدد التقارير</th><th>إجمالي الكمية</th><th>إجمالي المبيعات</th><th>الحصة</th></tr></thead><tbody id="branchTable"></tbody></table></div></div>
      </div>
'''
s=s[:start]+new+s[end:]
s=s.replace('let selectedBranch = branches[0], chartTop, chartProducts, chartTrend;','let selectedBranch = branches[0], chartTop, chartProducts, chartTrend, chartSalesShare, chartReportsShare;',1)
js_start=s.index('function renderOverview(){')
js_end=s.index('\nfunction renderBranches(){',js_start)
newjs=r'''function renderOverview(){
  const stats=branchStats(), items=allItems();
  const total=items.reduce((a,x)=>a+Number(x.sales||0),0), best=stats.find(x=>x.sales>0);
  const prod={}; items.forEach(x=>prod[x.name]=(prod[x.name]||0)+Number(x.qty||0));
  const top=Object.entries(prod).sort((a,b)=>b[1]-a[1])[0], reportCount=reports.length;
  $('kpiTotalSales').textContent=money(total); $('kpiBestBranch').textContent=best?.branch||'—'; $('kpiTopProduct').textContent=top?top[0]:'—'; $('kpiDeadCount').textContent=fmt(reportCount); $('salesShareCenter').textContent=money(total); $('reportsShareCenter').textContent=fmt(reportCount); $('branchTableCount').textContent=`(${stats.length})`;
  $('branchTable').innerHTML=stats.map(x=>{const pct=total?x.sales/total*100:0;return `<tr data-overview-branch="${x.branch}"><td>${x.branch}</td><td>${x.reports}</td><td>${fmt(x.qty)}</td><td>${money(x.sales)}</td><td>${pct.toLocaleString('ar-SA',{maximumFractionDigits:1})}%</td></tr>`}).join('');
  document.querySelectorAll('[data-overview-branch]').forEach(row=>row.onclick=()=>{selectedBranch=row.dataset.overviewBranch;document.querySelector('[data-view="branches"]')?.click()});
  drawCharts(stats);
}
function drawCharts(stats){
  if(!window.Chart)return; [chartTop,chartSalesShare,chartReportsShare].forEach(c=>{if(c)c.destroy()});
  const palette=['#8b6cf9','#2fd6c4','#e8479f','#f0a63a','#4c7dff','#55d98b','#ff6b75','#b56cf9'],active=stats.filter(x=>x.sales>0||x.reports>0),topBars=active.slice(0,7),grid='rgba(139,147,184,.10)',ticks='#8b93b8';
  const common={responsive:true,maintainAspectRatio:false,animation:{duration:850,easing:'easeOutQuart'},plugins:{legend:{display:false},tooltip:{backgroundColor:'#0e1424',titleColor:'#eef1fb',bodyColor:'#eef1fb',borderColor:'#232b4a',borderWidth:1,padding:10}}};
  chartTop=new Chart($('chartTopBranches'),{type:'bar',data:{labels:topBars.map(x=>x.branch),datasets:[{label:'المبيعات',data:topBars.map(x=>x.sales),backgroundColor:topBars.map((_,i)=>palette[i%palette.length]),borderRadius:7,borderSkipped:false,barPercentage:.62,categoryPercentage:.72}]},options:{...common,indexAxis:'y',onClick:(e,els)=>{if(els[0])focusOverviewBranch(topBars[els[0].index].branch)},scales:{x:{grid:{color:grid},ticks:{color:ticks,font:{size:9},callback:v=>Number(v).toLocaleString('ar-SA')}},y:{grid:{display:false},ticks:{color:'#d8dded',font:{size:10}}}}}});
  const donutBase={...common,cutout:'72%',onHover:(e,els)=>{e.native.target.style.cursor=els.length?'pointer':'default'},plugins:{...common.plugins,legend:{display:true,position:'bottom',labels:{color:ticks,usePointStyle:true,pointStyle:'circle',boxWidth:7,boxHeight:7,padding:10,font:{size:9}}}}};
  const sd=active.slice(0,5),so=active.slice(5).reduce((a,x)=>a+x.sales,0); chartSalesShare=new Chart($('chartSalesShare'),{type:'doughnut',data:{labels:sd.map(x=>x.branch).concat(so>0?['أخرى']:[]),datasets:[{data:sd.map(x=>x.sales).concat(so>0?[so]:[]),backgroundColor:palette,borderColor:'#141a30',borderWidth:3,hoverOffset:7}]},options:{...donutBase,onClick:(e,els)=>{const i=els[0]?.index;if(i!=null&&i<sd.length)focusOverviewBranch(sd[i].branch)}}});
  const rd=[...active].sort((a,b)=>b.reports-a.reports).slice(0,5),ro=active.filter(x=>!rd.includes(x)).reduce((a,x)=>a+x.reports,0); chartReportsShare=new Chart($('chartReportsShare'),{type:'doughnut',data:{labels:rd.map(x=>x.branch).concat(ro>0?['أخرى']:[]),datasets:[{data:rd.map(x=>x.reports).concat(ro>0?[ro]:[]),backgroundColor:['#2fd6c4','#e8479f','#f0a63a','#8b6cf9','#4c7dff','#55d98b'],borderColor:'#141a30',borderWidth:3,hoverOffset:7}]},options:{...donutBase,onClick:(e,els)=>{const i=els[0]?.index;if(i!=null&&i<rd.length)focusOverviewBranch(rd[i].branch)}}});
}
function focusOverviewBranch(branch){const row=document.querySelector(`[data-overview-branch="${CSS.escape(branch)}"]`);if(!row)return;document.querySelectorAll('[data-overview-branch]').forEach(r=>r.classList.toggle('is-focus',r===row));row.scrollIntoView({behavior:'smooth',block:'nearest'});}
'''
s=s[:js_start]+newjs+s[js_end:]
s=s.replace('<div class="demo-banner" id="demoBanner">','<div class="demo-banner" id="demoBanner" style="display:none;">',1)
p.write_text(s,encoding='utf-8')
print('Patched index.html')
