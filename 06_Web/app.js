'use strict';
const statusEl=document.querySelector('#form-status');
document.querySelector('#lead-form').addEventListener('submit',async event=>{
  event.preventDefault();const form=event.currentTarget;const button=form.querySelector('button');button.disabled=true;
  statusEl.textContent='Guardando tu consulta…';
  try{
    const response=await fetch('/api/contacts',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:form.elements.name.value,email:form.elements.email.value,privacy:form.elements.privacy.checked,marketing:form.elements.marketing.checked,website:form.elements.website.value})});
    const result=await response.json();if(!response.ok)throw new Error(result.error||'No se pudo guardar.');
    statusEl.textContent=result.message;
  }catch(error){statusEl.textContent=error.message||'Error de conexión. Inténtalo de nuevo más tarde.';}
  finally{button.disabled=false;}
});
function external(id,value){
  if(!value)return false;
  try{const url=new URL(value);if(url.protocol!=='https:')return false;const a=document.getElementById(id);a.href=url.href;a.rel='noopener noreferrer';a.hidden=false;return true;}catch{return false;}
}
fetch('/api/config').then(r=>r.json()).then(c=>{
  external('instagram',c.instagram_url);
  if(external('booking',c.booking_url))document.getElementById('booking-pending').hidden=true;
  // Keep payment unavailable until full offer details are provided.
  if(c.session_price&&c.currency&&c.session_duration){document.getElementById('session-details').textContent=`${c.session_duration} · ${c.session_price} ${c.currency}`;external('payment',c.payment_url);}
  if(external('community',c.community_url))document.getElementById('community-pending').hidden=true;
  if(/^\d{8,15}$/.test(c.whatsapp_number))external('whatsapp',`https://wa.me/${c.whatsapp_number}`);
}).catch(()=>{});
