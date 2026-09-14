from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

css='''<style id="video-match-v2">
:root{--bg:#090f22;--panel:#111a35;--border:#263253;--purple:#8b5cf6;--pink:#ff3e91;--blue:#4d7cff;--teal:#16d9bd;--amber:#ffc234;--text:#f5f7ff;--muted:#7f8bad}
body{background:radial-gradient(circle at 45% -10%,#1a2550 0,#0c142d 34%,#080e20 72%)}
.app{max-width:1240px;grid-template-columns:86px 1fr;gap:16px}.sidebar{border-radius:18px;background:linear-gradient(180deg,#111a35,#0e1730);box-shadow:0 18px 50px rgba(0,0,0,.22);padding:14px 7px}.nav-item{border-radius:12px;min-height:57px}.nav-item.active{background:linear-gradient(145deg,rgba(139,92,246,.28),rgba(255,62,145,.14));box-shadow:inset 0 0 0 1px rgba(139,92,246,.14)}
.top-bar{padding:10px 14px;border-radius:13px;background:linear-gradient(180deg,rgba(18,28,58,.96),rgba(15,23,48,.96));box-shadow:0 12px 34px rgba(0,0,0,.16)}.top-bar h1{font-size:14px}.top-bar .sub{font-size:9.5px}.select-box{height:32px;padding:0 10px;font-size:10px;border-radius:8px}
#view-overview .kpi-row{grid-template-columns:repeat(4,1fr);gap:10px;margin-top:0}#view-overview .kpi{min-height:64px;padding:11px 13px;border-radius:11px;background:linear-gradient(160deg,#151f40,#101831);box-shadow:0 12px 28px rgba(0,0,0,.17);border-color:#29365a}#view-overview .kpi::before{width:3px}#view-overview .kpi .label{font-size:9.5px;color:#8894b7;margin-bottom:6px}#view-overview .kpi .value{font-size:19px;line-height:1.15;font-weight:800}
#view-overview .dashboard-visual-grid{grid-template-columns:1fr 1.18fr 1fr;gap:10px;margin-top:10px}#view-overview .dashboard-visual-grid .panel,#view-overview .dashboard-table-panel{border-radius:12px;padding:12px 13px;background:linear-gradient(165deg,#131d3b,#0f1730);border-color:#283456;box-shadow:0 12px 30px rgba(0,0,0,.16)}#view-overview .dashboard-visual-grid h3,#view-overview .dashboard-table-panel h3{font-size:11px;margin-bottom:4px;color:#f0f3ff}#view-overview .dashboard-visual-grid h3 span,#view-overview .dashboard-table-panel h3 span{font-size:8px}#view-overview .donut-wrap,#view-overview .video-bar-wrap{height:190px}#view-overview .donut-wrap canvas{max-height:180px}#view-overview .chart-center b{font-size:16px}#view-overview .chart-center small{font-size:8px}#view-overview .dashboard-table-panel{margin-top:10px}#view-overview .controls{margin:7px 0 8px}.search-box{height:30px;font-size:10px}.mini-share{font-size:8px;padding:3px 7px}#view-overview table{font-size:10px}#view-overview th{font-size:9px;padding:8px 7px}#view-overview td{padding:8px 7px}.metric-bar{display:flex;align-items:center;gap:7px}.metric-bar-track{width:74px;height:5px;border-radius:99px;background:#182342;overflow:hidden}.metric-bar-fill{height:100%;border-radius:99px;background:linear-gradient(90deg,var(--teal),var(--purple));box-shadow:0 0 10px rgba(22,217,189,.35)}.status-pill{display:inline-flex;align-items:center;gap:5px;padding:3px 7px;border-radius:99px;border:1px solid rgba(22,217,189,.2);background:rgba(22,217,189,.08);color:#5cead7;font-size:8px}.status-pill:before{content:'';width:5px;height:5px;border-radius:50%;background:#20dfc4;box-shadow:0 0 8px #20dfc4}
@media(max-width:900px){.app{grid-template-columns:1fr;gap:10px;padding-bottom:10px}.sidebar{position:sticky;top:0;z-index:30;flex-direction:row;border-radius:0 0 16px 16px;padding:7px 8px;justify-content:space-around;background:rgba(12,19,41,.94);backdrop-filter:blur(14px)}.sidebar .brand{display:none}.nav-item{min-width:62px;min-height:48px;padding:7px 5px;font-size:8px}.main{gap:10px}.top-bar{margin:0 6px;padding:10px 12px}#view-overview{padding:0 6px}#view-overview .kpi-row{grid-template-columns:repeat(2,1fr);gap:8px}#view-overview .kpi{min-height:72px;padding:12px}#view-overview .dashboard-visual-grid{grid-template-columns:1fr;gap:8px}#view-overview .dashboard-visual-grid .panel:nth-child(2){grid-column:auto;order:-1}#view-overview .dashboard-visual-grid .panel{min-height:245px}#view-overview .donut-wrap,#view-overview .video-bar-wrap{height:210px}#view-overview table{min-width:620px}}
</style>'''
if 'id="video-match-v2"' not in s:
    s=s.replace('</head>',css+'</head>',1)

s=s.replace('نظرة عامة على كل الفروع','لوحة متابعة حركة الفروع',1).replace('آخر تحديث للبيانات','تحليل حي لحركة الأصناف والفروع',1)
start=s.index('      <div class="view active" id="view-overview">')
end=s.index('\n      <!-- ===== الفروع ===== -->',start)
overview='''      <div class="view active" id="view-overview">
        <div class="kpi-row">
          <div class="kpi" style="--accent:#8b5cf6"><div class="label">عدد الأصناف</div><div class="value mono" id="kpiTotalSales">—</div></div>
          <div class="kpi" style="--accent:#16d9bd"><div class="label">إجمالي الكمية</div><div class="value mono" id="kpiBestBranch">—</div></div>
          <div class="kpi" style="--accent:#ffc234"><div class="label">الفروع النشطة</div><div class="value mono" id="kpiTopProduct">—</div></div>
          <div class="kpi" style="--accent:#ff3e91"><div class="label">عدد التقارير</div><div class="value mono" id="kpiDeadCount">—</div></div>
        </div>
        <div class="dashboard-visual-grid">
          <div class="panel"><h3>توزيع الأصناف <span>أعلى الأصناف من إجمالي الحركة</span></h3><div class="donut-wrap"><canvas id="chartSalesShare"></canvas><div class="chart-center"><b id="salesShareCenter">—</b><small>صنف نشط</small></div></div></div>
          <div class="panel"><h3>أعلى الأصناف حركة <span>ترتيب حسب الكمية</span></h3><div class="video-bar-wrap"><canvas id="chartTopBranches"></canvas></div></div>
          <div class="panel"><h3>توزيع الفروع <span>مساهمة كل فرع في الحركة</span></h3><div class="donut-wrap"><canvas id="chartReportsShare"></canvas><div class="chart-center"><b id="reportsShareCenter">—</b><small>إجمالي الكمية</small></div></div></div>
        </div>
        <div class="panel dashboard-table-panel"><h3>تفاصيل حركة الأصناف <span id="branchTableCount"></span></h3><div class="controls"><input type="text" class="search-box" id="branchSearch" placeholder="ابحث باسم الصنف أو الفرع..."><span class="mini-share"><i></i> تتحدث تلقائياً من التقارير المرفوعة</span></div><div class="preview-scroll" style="max-height:320px;"><table><thead><tr><th>الصنف</th><th>الفرع</th><th>الكمية</th><th>الحصة</th><th>الحركة</th></tr></thead><tbody id="branchTable"></tbody></table></div></div>
      </div>
'''
s=s[:start]+overview+s[end:]
js_start=s.index('function renderOverview(){')
js_end=s.index('\nfunction renderBranches(){',js_start)
js='''function renderOverview(){
  const items=allItems(), productMap={}, branchMap={};
  items.forEach(x=>{const name=(x.name||'بدون اسم').trim(),branch=x.branch||'غير محدد',qty=Number(x.qty||0);productMap[name]=(productMap[name]||0)+qty;branchMap[branch]=(branchMap[branch]||0)+qty;});
  const products=Object.entries(productMap).map(([name,qty])=>({name,qty})).sort((a,b)=>b.qty-a.qty), branchQty=Object.entries(branchMap).map(([branch,qty])=>({branch,qty})).sort((a,b)=>b.qty-a.qty), totalQty=products.reduce((a,x)=>a+x.qty,0);
  $('kpiTotalSales').textContent=fmt(products.length);$('kpiBestBranch').textContent=fmt(totalQty);$('kpiTopProduct').textContent=fmt(branchQty.filter(x=>x.qty>0).length);$('kpiDeadCount').textContent=fmt(reports.length);$('salesShareCenter').textContent=fmt(products.length);$('reportsShareCenter').textContent=fmt(totalQty);
  const rows=[];reports.forEach(r=>(r.items||[]).forEach(x=>rows.push({name:x.name||'بدون اسم',branch:r.branch||'غير محدد',qty:Number(x.qty||0)})));rows.sort((a,b)=>b.qty-a.qty);$('branchTableCount').textContent=`(${rows.length})`;
  const renderRows=(q='')=>{const f=rows.filter(x=>!q||x.name.includes(q)||x.branch.includes(q)).slice(0,80);$('branchTable').innerHTML=f.map(x=>{const pct=totalQty?x.qty/totalQty*100:0;return `<tr><td><b>${x.name}</b></td><td>${x.branch}</td><td>${fmt(x.qty)}</td><td>${pct.toLocaleString('ar-SA',{maximumFractionDigits:1})}%</td><td><div class="metric-bar"><div class="metric-bar-track"><div class="metric-bar-fill" style="width:${Math.min(100,Math.max(4,pct*4))}%"></div></div><span class="status-pill">نشط</span></div></td></tr>`}).join('')};renderRows();$('branchSearch').oninput=e=>renderRows(e.target.value.trim());drawCharts(products,branchQty,totalQty);
}
function drawCharts(products,branchQty,totalQty){
  if(!window.Chart)return;[chartTop,chartSalesShare,chartReportsShare].forEach(c=>{if(c)c.destroy()});const palette=['#8b5cf6','#16d9bd','#ff3e91','#ffc234','#4d7cff','#5fe1ff','#ff6b75','#a3ff6b'];const common={responsive:true,maintainAspectRatio:false,animation:{duration:950,easing:'easeOutQuart'},plugins:{legend:{display:false},tooltip:{backgroundColor:'#0b132b',titleColor:'#fff',bodyColor:'#e9edff',borderColor:'#2a3960',borderWidth:1,padding:9,displayColors:true}},layout:{padding:4}};const top=products.slice(0,6);
  chartTop=new Chart($('chartTopBranches'),{type:'bar',data:{labels:top.map(x=>x.name.length>18?x.name.slice(0,18)+'…':x.name),datasets:[{data:top.map(x=>x.qty),backgroundColor:top.map((_,i)=>palette[i%palette.length]),borderRadius:4,borderSkipped:false,barPercentage:.56,categoryPercentage:.72}]},options:{...common,indexAxis:'y',scales:{x:{grid:{color:'rgba(117,137,184,.10)',drawBorder:false},ticks:{color:'#7f8bad',font:{size:8}}},y:{grid:{display:false},ticks:{color:'#dbe1f5',font:{size:8}}}}}});
  const dp=products.slice(0,5),otherP=products.slice(5).reduce((a,x)=>a+x.qty,0),donutOpts={...common,cutout:'66%',plugins:{...common.plugins,legend:{display:true,position:'bottom',labels:{color:'#8a96b9',usePointStyle:true,pointStyle:'circle',boxWidth:6,boxHeight:6,padding:7,font:{size:7}}}}};
  chartSalesShare=new Chart($('chartSalesShare'),{type:'doughnut',data:{labels:dp.map(x=>x.name.length>10?x.name.slice(0,10)+'…':x.name).concat(otherP>0?['أخرى']:[]),datasets:[{data:dp.map(x=>x.qty).concat(otherP>0?[otherP]:[]),backgroundColor:palette,borderColor:'#111a35',borderWidth:2,hoverOffset:6}]},options:donutOpts});
  const db=branchQty.slice(0,5),otherB=branchQty.slice(5).reduce((a,x)=>a+x.qty,0);chartReportsShare=new Chart($('chartReportsShare'),{type:'doughnut',data:{labels:db.map(x=>x.branch).concat(otherB>0?['أخرى']:[]),datasets:[{data:db.map(x=>x.qty).concat(otherB>0?[otherB]:[]),backgroundColor:['#16d9bd','#ff3e91','#ffc234','#8b5cf6','#4d7cff','#5fe1ff'],borderColor:'#111a35',borderWidth:2,hoverOffset:6}]},options:donutOpts});
}
function focusOverviewBranch(branch){}
'''
s=s[:js_start]+js+s[js_end:]
p.write_text(s,encoding='utf-8')
print('video-match-v2 applied')
