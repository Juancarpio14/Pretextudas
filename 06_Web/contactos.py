"""Administración local. No se expone un panel público."""
from pathlib import Path
import sqlite3, csv, argparse
p=argparse.ArgumentParser();p.add_argument('action',choices=['export','delete']);p.add_argument('--email');p.add_argument('--output',default='contactos_exportados.csv');p.add_argument('--marketing-only',action='store_true');args=p.parse_args()
db=Path(__file__).resolve().parent/'datos/contactos.sqlite3'
if not db.exists():raise SystemExit('Primero inicia server.py.')
with sqlite3.connect(db) as c:
    if args.action=='delete':
        if not args.email:raise SystemExit('Indica --email para eliminar un contacto.')
        c.execute('DELETE FROM contacts WHERE email=?',(args.email.strip().lower(),));print('Solicitud de eliminación procesada.')
    else:
        query='SELECT id,name,email,marketing,requested_at,consent_version FROM contacts'+(' WHERE marketing=1' if args.marketing_only else '')
        rows=c.execute(query).fetchall()
        def safe(v):
            text=str(v)
            return "'"+text if text.lstrip().startswith(('=','+','-','@')) else text
        with open(args.output,'w',newline='',encoding='utf-8-sig') as f:
            w=csv.writer(f);w.writerow(['id','nombre','correo','marketing','fecha_utc','version_consentimiento']);w.writerows([[safe(v) for v in row] for row in rows])
        print(f'Exportados {len(rows)} contactos. Guarda el archivo de forma privada.')
