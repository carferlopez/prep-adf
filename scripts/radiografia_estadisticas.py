"""
Estadísticas objetivas de redacción de las preguntas oficiales (forma del enunciado, polaridad, cita de
norma y artículo, longitudes, posición de la correcta, absolutos y normas citadas). Son las cifras de
las secciones 2 y 11 de notebooklm/01_radiografia_tribunal.md.

Uso:
    python3 scripts/radiografia_estadisticas.py notebooklm/datos/preguntas_oficiales_2023_2025.json \
        > notebooklm/datos/estadisticas_objetivas.txt
"""
import json,re,sys,statistics as st,collections
U=json.load(open(sys.argv[1], encoding="utf-8"))
K=[u for u in U if u["prueba"]!="Inglés"]
def pct(n,d): return f"{n}/{d} ({100*n/d:.0f}%)"
def stats(Q,label):
    n=len(Q); A=[q for q in Q if q["correcta"]]
    out={"grupo":label,"n":n,"con_respuesta":len(A)}
    e=[q["enunciado"] for q in Q]
    out["termina_?"]=pct(sum(s.rstrip().endswith("?") for s in e),n)
    out["termina_:"]=pct(sum(s.rstrip().endswith(":") for s in e),n)
    out["termina_..."]=pct(sum(s.rstrip().endswith(("...","…")) for s in e),n)
    out["abre_citando_norma"]=pct(sum(bool(re.match(r"(Según|Conforme|De acuerdo|A tenor|Acorde|En virtud|De conformidad|En la Ley|En relación|Atendiendo|Señal\w+ la opción \w+: Según)",s)) for s in e),n)
    out["menciona_norma_en_enunciado"]=pct(sum(bool(re.search(r"\b(Ley|Real Decreto|RD|Reglamento|Declaraci[óo]n (sobre la |de )?Red|Estatuto|LO|Orden|Directiva|Esquema Nacional)\b",s)) for s in e),n)
    out["cita_articulo"]=pct(sum(bool(re.search(r"art(í|i)culo|art\.",s,re.I)) for s in e),n)
    out["negativa"]=pct(sum(bool(re.search(r"\bNO\b|INCORRECTA|FALSA|excepto|no se contempla|no es|NO es",s)) for s in e),n)
    out["negativa_mayusculas"]=pct(sum(bool(re.search(r"\bNO\b|INCORRECTA|FALSA",s)) for s in e),n)
    out["pide_correcta_explicita"]=pct(sum(bool(re.search(r"CORRECTA|correcta|cierta|verdadera",s)) and not re.search(r"INCORRECTA",s) for s in e),n)
    out["supuesto_practico"]=pct(sum(bool(re.search(r"\b(una empresa|un trabajador|una persona|En el año|ha sido sancionad|supuesto|Juan|María)\b",s,re.I)) for s in e),n)
    L=[len(s) for s in e]; out["long_enunciado_mediana"]=st.median(L); out["long_enunciado_max"]=max(L)
    ol=[len(o) for q in Q for o in q["opciones"]]; out["long_opcion_mediana"]=st.median(ol)
    pos=collections.Counter(q["correcta"] for q in A); out["posicion_correcta"]={k:pct(pos[k],len(A)) for k in "ABCD"}
    longest=sum(len(q["opciones"]["ABCD".index(q["correcta"])])==max(map(len,q["opciones"])) for q in A)
    shortest=sum(len(q["opciones"]["ABCD".index(q["correcta"])])==min(map(len,q["opciones"])) for q in A)
    out["correcta_es_la_mas_larga"]=pct(longest,len(A)); out["correcta_es_la_mas_corta"]=pct(shortest,len(A))
    # opciones con prefijo común (estructura paralela)
    def prefix(q):
        p=q["opciones"][0]
        for o in q["opciones"][1:]:
            i=0
            while i<min(len(p),len(o)) and p[i]==o[i]: i+=1
            p=p[:i]
        return len(p.strip())
    out["opciones_con_prefijo_comun>=10car"]=pct(sum(prefix(q)>=10 for q in Q),n)
    out["opciones_numericas"]=pct(sum(all(re.search(r"\d|\b(uno|dos|tres|cuatro|cinco|seis|diez|quince|veinte|treinta|mes|meses|años|días)\b",o) for o in q["opciones"]) for q in Q),n)
    out["opcion_absoluta(siempre/nunca/en ningún caso/exclusivamente/solo/en todo caso)"]=pct(sum(any(re.search(r"\b(siempre|nunca|en ningún caso|exclusivamente|únicamente|solo|sólo|en todo caso|cualquier)\b",o,re.I) for o in q["opciones"]) for q in Q),n)
    abs_corr=sum(bool(re.search(r"\b(siempre|nunca|en ningún caso|exclusivamente|únicamente|solo|sólo|en todo caso|cualquier)\b",q["opciones"]["ABCD".index(q["correcta"])],re.I)) for q in A)
    abs_tot=sum(sum(bool(re.search(r"\b(siempre|nunca|en ningún caso|exclusivamente|únicamente|solo|sólo|en todo caso|cualquier)\b",o,re.I)) for o in q["opciones"]) for q in A)
    out["absolutos: veces que la opción con absoluto es la correcta"]=f"{abs_corr} de {abs_tot} opciones con absoluto"
    out["todas/ninguna_anteriores"]=pct(sum(any(re.search(r"(todas|ninguna) (de )?las (anteriores|respuestas)",o,re.I) for o in q["opciones"]) for q in Q),n)
    return out
res=[stats(K,"CONOCIMIENTOS (126)")]
for g in sorted({u["prueba"]+" | "+u["convocatoria"] for u in K}):
    res.append(stats([u for u in K if u["prueba"]+" | "+u["convocatoria"]==g],g))
res.append(stats([u for u in U if u["prueba"]=="Inglés"],"INGLÉS (54)"))
# normas
NORMAS=[("Ley 39/2015 (LPACAP)",r"39/2015"),("Ley 40/2015 (LRJSP)",r"40/2015"),("Ley 9/2017 (LCSP)",r"9/2017|Contratos del Sector P"),
("Ley 38/2015 Sector Ferroviario",r"38/2015|Sector Ferroviario\b(?! -)"),("RD 2387/2004 Reglamento Sector Ferroviario",r"2387/2004|Reglamento del Sector Ferroviario"),
("Estatuto ADIF RD 2395/2004",r"2395/2004|Estatuto (del|de la entidad)|Estatuto del ADIF|según su Estatuto"),("Declaración sobre la Red",r"Declaraci[óo]n (sobre la|de) Red"),
("Reglamento (UE) 402/2013 (MCS riesgos)",r"402/2013"),("Reglamento Delegado (UE) 2018/762 (SGS)",r"762"),("RD 929/2020 seguridad operacional",r"929/20"),
("Ley 31/1995 PRL",r"31/1995|PRL|Prevenci[óo]n de Riesgos"),("LO 3/2018 Protección de Datos",r"3/2018|3/18|Protecci[óo]n de Datos"),("RD 311/2022 ENS",r"311/2022|Esquema Nacional de Seguridad"),
("LO 3/2007 Igualdad",r"3/2007"),("Ley 4/2023 trans/LGTBI",r"4/2023"),("Ley 53/1984 Incompatibilidades",r"53/1984"),("TREBEP RDL 5/2015",r"5/2015|Estatuto B[áa]sico"),
("ET RDL 2/2015",r"2/2015|Estatuto de los Trabajadores"),("LGSS RDL 8/2015",r"8/2015|[Ss]eguridad [Ss]ocial"),("Ley 47/2003 LGP",r"47/2003|General Presupuestaria"),
("Ley 21/2013 Evaluación ambiental",r"21/2013|evaluaci[óo]n ambiental"),("Ley 19/2013 Transparencia",r"19/2013|Transparencia"),("Canal ético / antifraude Adif",r"Canal [ÉE]tico|fraude"),
("Ley 2/2023 informantes",r"2/2023"),("Ley 22/2021 / PGE",r"Presupuestos Generales"),
]
nc=collections.Counter(); nogrp=[]
for q in K:
    txt=q["enunciado"]+" "+" ".join(q["opciones"]); hit=False
    for name,rx in NORMAS:
        if re.search(rx,q["enunciado"]) or (name.startswith("Estatuto ADIF") and re.search(r"Estatuto del ADIF|Estatuto de la entidad|según su Estatuto",txt)):
            nc[(name,q["prueba"].split(" (")[0]+(" Gestión" if "Gestión" in q["prueba"] else ""))]+=1; hit=True; break
    if not hit: nogrp.append((q["id"],q["enunciado"][:120]))
print(json.dumps(res,ensure_ascii=False,indent=1))
tab=collections.defaultdict(dict)
for (n,p),c in nc.items(): tab[n][p]=c
print("\nNORMAS (por enunciado, 1ª coincidencia):")
for n,d in sorted(tab.items(),key=lambda x:-sum(x[1].values())): print(f"  {sum(d.values()):3d}  {n}: {d}")
print("SIN NORMA DETECTADA:", nogrp)
