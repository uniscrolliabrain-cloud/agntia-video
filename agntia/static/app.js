'use strict';
const $ = id => document.getElementById(id);
let project = null, dirty = false, status = null, pollTimer = null, toastTimer = null, activeJobs = new Set();
const kindNames = {preview:'Previsualización',export:'Exportación',analysis:'Análisis de material',chat:'Agente de edición',import:'Importación de carpeta',beats:'Detección de beats'};

function node(tag, text, cls) { const el = document.createElement(tag); if(text !== undefined) el.textContent = text; if(cls) el.className = cls; return el; }
function toast(message, error=false) { $('toast').textContent=message; $('toast').className=error?'error':''; $('toast').hidden=false; clearTimeout(toastTimer); toastTimer=setTimeout(()=>{$('toast').hidden=true;},error?12000:5000); }
async function api(url, options={}) {
  const opts={...options};
  if(opts.body && !(opts.body instanceof FormData)){opts.headers={...opts.headers,'Content-Type':'application/json'};opts.body=JSON.stringify(opts.body);}
  const response=await fetch(url,opts);
  if(response.status===401){if(!$('login-dialog').open)$('login-dialog').showModal();throw new Error('Introduce tu token de acceso');}
  if(!response.ok){let data;try{data=await response.json();}catch{data={detail:`Error HTTP ${response.status}`};}throw new Error(typeof data.detail==='string'?data.detail:'Revisa los campos del montaje');}
  return response.json();
}
function action(fn){return async event=>{try{await fn(event);}catch(error){toast(error.message,true);}};}
function markDirty(){dirty=true;$('save-state').textContent='Cambios sin guardar';}
function time(seconds){const s=Math.round(seconds||0);return `${String(Math.floor(s/60)).padStart(2,'0')}:${String(s%60).padStart(2,'0')}`;}
function total(){return project?.plan.segments.reduce((sum,s)=>sum+Math.max(0,s.end-s.start),0)||0;}
function setTotal(){$('duration').textContent=time(total());}

function readAudioSettings(){
  return {voice_enhancement:$('voice-mode').value,voice_strength:Number($('voice-strength').value)/100,
    music:{asset_id:$('music-asset').value||null,volume:Number($('music-volume').value)/100,start:Number($('music-start').value),
      loop:$('music-loop').checked,ducking:$('music-ducking').checked,fade_seconds:Number($('music-fade').value)}};
}
function drawAudioControls(){
  const settings=project.settings,music=settings.music||{};
  $('voice-mode').value=settings.voice_enhancement||'off';$('voice-strength').value=(settings.voice_strength??.8)*100;
  $('voice-strength-value').textContent=`${$('voice-strength').value}%`;
  const select=$('music-asset');select.replaceChildren(new Option('Sin música',''));
  project.assets.filter(a=>a.has_audio).forEach(a=>select.append(new Option(a.name,a.id)));select.value=music.asset_id||'';
  $('music-volume').value=(music.volume??.15)*100;$('music-volume-value').textContent=`${$('music-volume').value}%`;
  $('music-start').value=music.start||0;$('music-fade').value=music.fade_seconds??1;$('music-loop').checked=music.loop??true;$('music-ducking').checked=music.ducking??true;
  const ready=status?.audio?.voice_ai;$('voice-ai-status').textContent=ready?'IA local disponible · sin API ni coste por minuto. Reduce ruido; no reconstruye una grabación saturada.':'IA local no disponible: instala FFmpeg con arnndn. Puedes usar la limpieza clásica.';
  $('voice-mode').querySelector('option[value="ai"]').disabled=!ready;
  drawBeatInfo();
}
function drawBeatInfo(){
  const asset=project.assets.find(a=>a.id===$('music-asset').value),beats=asset?.beats;
  $('beat-info').textContent=beats?`${beats.times.length} golpes detectados${beats.bpm?` · ≈ ${beats.bpm} BPM`:''}. Revisa el resultado antes de ajustar.`:asset?'Música seleccionada. Detecta sus golpes para guiar los cortes.':'Elige una pista musical para detectar sus golpes.';
  $('detect-beats').disabled=!asset;$('snap-beats').disabled=!beats?.times?.length;
  $('undo-beats').hidden=!project.beat_undo||JSON.stringify(project.beat_undo.after)!==JSON.stringify(project.plan);
  const holder=$('beat-markers');holder.replaceChildren();
  if(!beats?.times?.length){holder.append(node('span','Los marcadores de ritmo aparecerán aquí.'));return;}
  const ns='http://www.w3.org/2000/svg',svg=document.createElementNS(ns,'svg');svg.setAttribute('viewBox','0 0 1000 60');svg.setAttribute('role','img');svg.setAttribute('aria-label',`${beats.times.length} golpes a lo largo de ${time(asset.duration)} de música`);
  const baseline=document.createElementNS(ns,'line');for(const [k,v] of Object.entries({x1:0,x2:1000,y1:45,y2:45,stroke:'#414557'}))baseline.setAttribute(k,v);svg.append(baseline);
  const step=Math.max(1,Math.ceil(beats.times.length/3000));
  beats.times.forEach((t,i)=>{if(i%step)return;const line=document.createElementNS(ns,'line');for(const [k,v] of Object.entries({x1:t/asset.duration*1000,x2:t/asset.duration*1000,y1:i%4===0?10:23,y2:45,stroke:i%4===0?'#c5b2ff':'#80739e','stroke-width':2}))line.setAttribute(k,v);const title=document.createElementNS(ns,'title');title.textContent=`${t.toFixed(2)} s`;line.append(title);svg.append(line);});holder.append(svg);
}

async function boot(){
  status=await api('/api/status');
  for(const name of ['deepseek','gemini']){$(`${name}-dot`).className=`dot ${status.providers[name]?'green':''}`;$(`${name}-label`).textContent=status.providers[name]?'Conectado':'Pendiente';}
  $('agent-hint').textContent=status.providers.deepseek?'DeepSeek · listo para tu briefing':'Configura DeepSeek o escribe el briefing abajo';
  if(!status.ffmpeg)toast('FFmpeg no está instalado. Lo necesitarás para analizar y renderizar.',true);
  await loadProjects();
}
async function loadProjects(selected){
  const projects=await api('/api/projects');const select=$('project-select');select.replaceChildren();
  select.append(new Option('Selecciona un proyecto',''));
  projects.forEach(p=>select.append(new Option(p.name,p.id)));
  const current=selected||localStorage.getItem('agntia-project');
  if(projects.some(p=>p.id===current)){select.value=current;await openProject(current);}
}
async function openProject(id){
  clearTimeout(pollTimer);activeJobs=new Set();dirty=false;
  if(!id){project=null;$('workspace').hidden=true;$('welcome').hidden=false;return;}
  project=await api(`/api/projects/${id}`);localStorage.setItem('agntia-project',id);
  $('welcome').hidden=true;$('workspace').hidden=false;
  $('player').hidden=true;$('player').pause();$('player').removeAttribute('src');$('player-empty').hidden=false;
  $('preview-description').textContent='Todavía no hay una previsualización';
  drawProject();await pollJobs(true);
}
function drawProject(){
  $('project-title').textContent=project.name;$('save-state').textContent='Guardado';
  $('briefing').value=project.briefing;
  $('source-language').value=project.settings.source_language;$('subtitles').value=project.settings.subtitles;$('fit').value=project.settings.fit;
  $('download-plan').href=`/api/projects/${project.id}/download-plan`;
  drawAssets();drawTimeline();drawMessages();drawAudioControls();
}
function drawMessages(){
  if(!project.messages.length)return;
  const list=$('chat-messages');list.replaceChildren();
  for(const message of project.messages){const div=node('div',undefined,`message ${message.role==='user'?'user':'assistant'}`);div.append(node('small',message.role==='user'?'TÚ':'AGNTIA'),node('span',message.content));list.append(div);}
  list.scrollTop=list.scrollHeight;
}
function drawAssets(){
  $('assets').replaceChildren();$('asset-count').textContent=`${project.assets.length} archivo${project.assets.length===1?'':'s'}`;
  for(const a of project.assets){
    const row=node('div',undefined,'asset');row.append(node('div',a.has_video?'▷':'♫','asset-icon'));
    const info=node('div',undefined,'asset-info');info.append(node('strong',a.name),node('small',`${time(a.duration)} · ${a.has_video?'Vídeo':'Audio'} · ${a.analysis?'Analizado':'Sin analizar'}`));row.append(info);
    const role=node('select');role.setAttribute('aria-label',`Función de ${a.name}`);
    for(const [value,label] of [['dialogue','Diálogo'],['avatar','Avatar'],['broll','B-roll'],['audio','Audio'],['music','Música']])role.append(new Option(label,value));role.value=a.role;
    role.addEventListener('change',action(async()=>{if(dirty)await saveProject();await api(`/api/projects/${project.id}/assets/${a.id}`,{method:'PATCH',body:{role:role.value}});project=await api(`/api/projects/${project.id}`);drawProject();}));row.append(role);
    const preview=node('button','Ver','outline');preview.addEventListener('click',()=>showVideo(`/api/projects/${project.id}/assets/${a.id}/media`,`${a.name} · archivo original`));row.append(preview);
    $('assets').append(row);
  }
}
function assetSelect(value,onChange,audio=false){
  const select=node('select');
  if(audio)select.append(new Option('Audio del mismo archivo',''));
  else select.append(new Option('Selecciona un archivo',''));
  project.assets.filter(a=>!audio||a.has_audio).forEach(a=>select.append(new Option(a.name,a.id)));
  select.value=value||'';select.addEventListener('change',()=>onChange(select.value));return select;
}
function labeled(text,input){const label=node('label',text);label.append(input);return label;}
function numberInput(value,onChange){const input=node('input');input.type='number';input.min='0';input.step='0.01';input.value=value??'';input.addEventListener('input',()=>{onChange(input.value===''?null:Number(input.value));markDirty();setTotal();});return input;}
function drawTimeline(){
  const segments=$('segments');segments.replaceChildren();
  project.plan.segments.forEach((s,index)=>{
    const row=node('div',undefined,'segment'),top=node('div',undefined,'segment-top'),controls=node('div',undefined,'segment-controls');
    top.append(node('strong',`CORTE ${String(index+1).padStart(2,'0')}`));
    for(const [label,title,fn] of [['↑','Subir corte',()=>{if(index>0)[project.plan.segments[index-1],project.plan.segments[index]]=[s,project.plan.segments[index-1]];}],['↓','Bajar corte',()=>{if(index<project.plan.segments.length-1)[project.plan.segments[index+1],project.plan.segments[index]]=[s,project.plan.segments[index+1]];}],['×','Eliminar corte',()=>project.plan.segments.splice(index,1)]]){const button=node('button',label);button.title=title;button.setAttribute('aria-label',title);button.addEventListener('click',()=>{fn();markDirty();drawTimeline();});controls.append(button);}
    top.append(controls);row.append(top);
    const fields=node('div',undefined,'segment-fields');
    fields.append(labeled('Imagen / archivo',assetSelect(s.asset_id,value=>{s.asset_id=value;markDirty();})),labeled('Inicio (s)',numberInput(s.start,v=>s.start=v)),labeled('Final (s)',numberInput(s.end,v=>s.end=v)));row.append(fields);
    const audio=node('div',undefined,'segment-fields audio-fields');audio.append(labeled('Pista de audio',assetSelect(s.audio_id,value=>{s.audio_id=value||null;if(!value)s.audio_start=null;markDirty();drawTimeline();},true)),labeled('Inicio audio (s)',numberInput(s.audio_start,v=>{s.audio_start=v;})));row.append(audio);
    const note=node('input');note.value=s.note||'';note.placeholder='Por qué conservar este corte';note.addEventListener('input',()=>{s.note=note.value;markDirty();});row.append(labeled('Nota de edición',note));row.lastChild.className='note-label';segments.append(row);
  });
  const clips=$('clips');clips.replaceChildren();
  project.plan.clips.forEach((c,index)=>{const row=node('div',undefined,'clip'),name=node('input');name.value=c.title;name.maxLength=120;name.addEventListener('input',()=>{c.title=name.value;markDirty();});row.append(labeled('Título del clip',name),labeled('Inicio podcast (s)',numberInput(c.start,v=>c.start=v)),labeled('Final podcast (s)',numberInput(c.end,v=>c.end=v)));const remove=node('button','×');remove.setAttribute('aria-label','Eliminar clip');remove.addEventListener('click',()=>{project.plan.clips.splice(index,1);markDirty();drawTimeline();});row.append(remove);clips.append(row);});
  setTotal();
}
async function saveProject(){
  if(!project)throw new Error('Crea un proyecto primero');
  const body={revision:project.revision,briefing:$('briefing').value,settings:{...readAudioSettings(),source_language:$('source-language').value,subtitles:$('subtitles').value,fit:$('fit').value},plan:project.plan};
  project=await api(`/api/projects/${project.id}`,{method:'PUT',body});dirty=false;$('save-state').textContent='Guardado';return project;
}
async function uploadFiles(files, asMusic=false){
  if(!project)throw new Error('Crea un proyecto primero');
  if(dirty)await saveProject();
  const pid=project.id;$('upload').disabled=true;
  let lastAsset=null;
  try{for(const [index,file] of [...files].entries()){toast(`Subiendo ${index+1}/${files.length}: ${file.name}`);const form=new FormData();form.append('file',file);lastAsset=await api(`/api/projects/${pid}/upload`,{method:'POST',body:form});if(asMusic)await api(`/api/projects/${pid}/assets/${lastAsset.id}`,{method:'PATCH',body:{role:'music'}});}if(project.id===pid){project=await api(`/api/projects/${pid}`);if(asMusic&&lastAsset)project.settings.music.asset_id=lastAsset.id;drawProject();if(asMusic){markDirty();await saveProject();}}toast('Material añadido a la biblioteca');}
  finally{$('upload').disabled=false;$('upload').value='';}
}
function showVideo(url,description){$('player').src=url;$('player').hidden=false;$('player-empty').hidden=true;$('preview-description').textContent=description;$('studio').scrollIntoView({behavior:'smooth'});}
async function startJob(path,body){
  await saveProject();const job=await api(`/api/projects/${project.id}/${path}`,{method:'POST',...(body?{body}:{})});activeJobs.add(job.id);toast('Trabajo añadido a la cola');await pollJobs();
}
function drawJobs(values){
  const list=$('jobs');list.replaceChildren();
  if(!values.length){list.append(node('p','Aquí aparecerán tus previsualizaciones y exportaciones.','muted'));return;}
  for(const job of values){const div=node('div',undefined,`job ${job.status}`),header=node('div',undefined,'job-header');header.append(node('strong',kindNames[job.kind]||job.kind),node('small',({done:'Completado',error:'Revisar',queued:'En cola',running:'En curso'})[job.status]));div.append(header,node('p',job.message));
    if(job.revision!==undefined&&job.revision!==project.revision)div.append(node('p','Este resultado corresponde a una versión anterior del montaje.'));
    for(const output of job.outputs||[]){const row=node('div',undefined,'output-row');row.append(node('span',output.name));const view=node('button','▷ Ver','outline');view.addEventListener('click',()=>showVideo(output.url,`${output.name} · ${job.mode==='preview'?'previsualización':'exportación'}`));const link=node('a','↓ MP4','text-link');link.href=output.url;link.download=`${output.name}.mp4`;row.append(view,link);if(output.srt){const srt=node('a','↓ SRT','text-link');srt.href=output.srt;srt.download=`${output.name}.srt`;row.append(srt);}div.append(row);}list.append(div);
  }
}
async function pollJobs(initial=false){
  clearTimeout(pollTimer);if(!project)return;
  const pid=project.id;
  try{const values=await api(`/api/projects/${pid}/jobs`);if(project?.id!==pid)return;
    let changed=false;
    for(const job of values){if(['queued','running'].includes(job.status)){activeJobs.add(job.id);}else if(activeJobs.has(job.id)){activeJobs.delete(job.id);if(job.status==='error')toast(job.message,true);else{toast(`${kindNames[job.kind]} terminado`);changed=true;if(job.kind==='preview'&&job.outputs?.length)showVideo(job.outputs[0].url,'Podcast · previsualización');}}}
    if(changed&&!dirty){project=await api(`/api/projects/${pid}`);drawProject();}
    if(initial){const last=values.find(j=>j.status==='done'&&j.kind==='preview'&&j.outputs?.length);if(last)showVideo(last.outputs[0].url,'Última previsualización guardada');}
    drawJobs(values);
  }catch(error){toast(error.message,true);}
  pollTimer=setTimeout(()=>pollJobs(),3000);
}

$('new-project').addEventListener('click',()=>$('new-dialog').showModal());$('welcome-create').addEventListener('click',()=>$('new-dialog').showModal());$('cancel-new').addEventListener('click',()=>$('new-dialog').close());
$('new-form').addEventListener('submit',action(async event=>{event.preventDefault();if(project&&dirty)await saveProject();const p=await api('/api/projects',{method:'POST',body:{name:$('new-name').value}});$('new-dialog').close();$('new-name').value='';await loadProjects(p.id);}));
$('project-select').addEventListener('change',action(async event=>{const value=event.target.value;if(project&&dirty)await saveProject();await openProject(value);}));
$('login-form').addEventListener('submit',async event=>{event.preventDefault();try{await api('/api/login',{method:'POST',body:{token:$('token').value}});$('token').value='';$('login-dialog').close();await boot();}catch(error){$('login-error').textContent=error.message;}});
$('upload').addEventListener('change',action(event=>uploadFiles(event.target.files)));
for(const type of ['dragenter','dragover'])$('upload-zone').addEventListener(type,event=>{event.preventDefault();$('upload-zone').classList.add('dragging');});
for(const type of ['dragleave','drop'])$('upload-zone').addEventListener(type,event=>{event.preventDefault();$('upload-zone').classList.remove('dragging');});
$('upload-zone').addEventListener('drop',action(event=>uploadFiles(event.dataTransfer.files)));
$('import-inbox').addEventListener('click',action(()=>startJob('import-inbox')));
$('analyze-button').addEventListener('click',action(()=>startJob('analyze')));
$('preview-button').addEventListener('click',action(()=>startJob('render',{mode:'preview'})));
$('export-button').addEventListener('click',action(()=>startJob('render',{mode:'export'})));
$('save-button').addEventListener('click',action(async()=>{await saveProject();toast('Montaje guardado');}));
for(const id of ['briefing','source-language','subtitles','fit'])$(id).addEventListener('input',markDirty);
$('add-segment').addEventListener('click',()=>{if(!project.assets.length){toast('Añade material a la biblioteca primero');return;}const a=project.assets.find(a=>a.role!=='broll'&&a.role!=='music')||project.assets[0];project.plan.segments.push({asset_id:a.id,start:0,end:a.duration,audio_id:null,audio_start:null,note:''});markDirty();drawTimeline();});
$('add-clip').addEventListener('click',()=>{if(!total()){toast('Añade un corte al podcast primero');return;}project.plan.clips.push({title:`Clip ${project.plan.clips.length+1}`,start:0,end:Math.min(total(),60)});markDirty();drawTimeline();});
$('chat-form').addEventListener('submit',action(async event=>{event.preventDefault();const message=$('chat-input').value.trim();if(!message)return;await startJob('chat',{message});$('chat-input').value='';}));
$('music-upload').addEventListener('change',action(async event=>{try{await uploadFiles(event.target.files,true);}finally{event.target.value='';}}));
for(const id of ['voice-mode','voice-strength','music-asset','music-volume','music-start','music-fade','music-loop','music-ducking']){
  $(id).addEventListener('input',()=>{markDirty();$('voice-strength-value').textContent=`${$('voice-strength').value}%`;$('music-volume-value').textContent=`${$('music-volume').value}%`;if(id==='music-asset')drawBeatInfo();});
}
$('detect-beats').addEventListener('click',action(async()=>{const aid=$('music-asset').value;if(!aid)throw new Error('Elige una música primero');await startJob(`assets/${aid}/beats`);}));
$('snap-beats').addEventListener('click',action(async()=>{await saveProject();const result=await api(`/api/projects/${project.id}/snap-beats`,{method:'POST',body:{revision:project.revision,tolerance:Number($('beat-tolerance').value),minimum:.5}});project=result.project;dirty=false;drawProject();toast(result.changed?`${result.changed} cortes ajustados. Genera una previsualización para revisarlos.`:'No hay cortes que se puedan acercar a un beat dentro del margen y los límites del material.');}));
$('undo-beats').addEventListener('click',action(async()=>{if(dirty)await saveProject();project=await api(`/api/projects/${project.id}/undo-beats`,{method:'POST',body:{revision:project.revision}});dirty=false;drawProject();toast('Ajuste de beats deshecho');}));
window.addEventListener('beforeunload',event=>{if(dirty){event.preventDefault();event.returnValue='';}});
boot().catch(error=>toast(error.message,true));
